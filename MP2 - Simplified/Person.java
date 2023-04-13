//Person Pseudocode

import java.security.SecureRandom;
import java.util.concurrent.Semaphore;

//Threaded as Person is the thread as per specifications.
public class Person extends Thread{
	private String color = null;
    private int roomNo = -1;
    private long fittingTime = 0; //In ms
    private boolean fitted = false;
    static Semaphore s = null; //All Persons refer to the same Semaphore & permits.
    private static FittingRoom fittingRoom = null; //All Persons refer to the same fitting room.
	
	public Person(	String color, Semaphore sem, 
					FittingRoom newFittingRoom, long fittingLimit){
        this.color = color;
        s = sem;
        fittingRoom = newFittingRoom;
        this.fittingTime = getNewFittingTime(fittingLimit);
    }
	
	//Generate a randomized time from 1000ms to the given fittingLimit
	private long getNewFittingTime(long fittingLimit){
        return new SecureRandom().nextLong(1000, fittingLimit);
    }
	
	@Override
	public void run(){
		try{
			while(!fitted){
				if(	fittingRoom.isAllowedEntry() && 
					fittingRoom.isMatching(this) && 
					s.tryAcquire(1)){ //If tryAcquire() True, it had acquired a permit.
					//<<START: CRITICAL SECTION>>
					
					this.roomNo = fittingRoom.enterRoom(this);
					if(this.roomNo == -1) //No room available despite allowed
                        continue;
                    
                    //"Do fitting room stuff"
                    Thread.sleep(this.getFittingTime());
                    this.fitted = true;

                    if(fittingRoom.isLastPerson(this)){ //Close Room
                        System.out.println(selfStr() + "Empty fitting room");
                        fittingRoom.closeFittingRoom();
                    }else{ //Just exit
                        fittingRoom.exitRoom(this);
                    }
					
					//<<END: CRITICAL SECTION>>
                    //Give permit to other Persons/Return to permits pool.
                    s.release();
				}
			}
		}catch(InterruptedException ex){}
		return;
	}
	
	//Check if the Person has already been fitted.
    public boolean isFitted(){
        return this.fitted;
    }

    //Set a person's room number
    public void setRoomNo(int roomNo){
        this.roomNo = roomNo;
    }

    //Get the room number a person is in.
    public int getRoomNo(){
        return this.roomNo;
    }
	
	//Get the ID of the person
    public long getID(){
        return this.getId();
    }

    //Get the color of the person
    public String getColor(){
        return this.color;
    }

	//Get Person's fittingTime
    public long getFittingTime(){
        return this.fittingTime;
    }

    //Get the basic stringified details of the person 
    public String selfStr(){
        return getId() + " (" + getColor() + ", " + getFittingTime() + "ms) ";
    }

    //Print the stringified version if the Person obj.
    public void printSelf(){
        System.out.println(selfStr());
    }
}