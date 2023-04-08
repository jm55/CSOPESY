/**
 * CSOPESY - Process Scheduling
 * 
 * de Veyra, Escalona, Naval, Villavicencio
 */

import java.security.SecureRandom;
import java.util.concurrent.Semaphore;

public class Person extends Thread{
    private String color = null;
    private int roomNo = -1;
    private long fittingTime = 0; //In ms
    private boolean fitted = false;
    static Semaphore s = null; //All persons must recognize the same no. of semaphores, thus a static value.
    private static FittingRoom fittingRoom = null;
    /**
     * Constructor for a person
     * @param id
     * @param color
     * @param sem
     * @param fittingRoom
     */
    public Person(String color, Semaphore sem, FittingRoom newFittingRoom, long fittingLimit){
        this.color = color;
        s = sem;
        fittingRoom = newFittingRoom;
        this.fittingTime = getNewFittingTime(fittingLimit);
        //System.out.println(this.selfStr() + " Fitting Time: " + this.fittingTime + "ms");
    }

    /**
     * Generates the fittingTime for the Person
     * @param fittingLimit
     * @return fittingTime for this Person obj.
     */
    private long getNewFittingTime(long fittingLimit){
        return new SecureRandom().nextLong(1000, fittingLimit);
    }
    
    @Override
    public void run(){
        try {
            //While person have not fitted
            while(!fitted){
                 /**
                 * Check ff. before CRITICAL SECTION:
                 * 0. Check if entry is allowed
                 * 1. There is at least 1 room available.
                 * 2. Check if there is a permit available
                 * 
                 * A semaphore will be acquired once s.tryAcquire() is true, thus the beginning of the Critical Section. 
                 */
                if(fittingRoom.isAllowedEntry() && fittingRoom.isMatching(this) && s.tryAcquire(1)){ //<---s.tryAcquire() substitutes for s.acquire();
                    
                    //<<<BEGINNING OF CRITICAL SECTION>>>
                    
                    this.roomNo = fittingRoom.enterRoom(this);
                    if(this.roomNo == -1) //Skip if room no. given is -1 (i.e., no room)
                        continue;
                    
                    //"Do fitting room stuff"
                    Thread.sleep(this.getFittingTime());
                    this.fitted = true;

                    /**
                     * If the fittingRoom is the last person, close the fittingRoom.
                     * Else just exit the room.
                     */
                    if(fittingRoom.isLastPerson(this)){
                        //System.out.println(this.selfStr() + " Last to leave room " + this.roomNo);
                        System.out.println(selfStr() + "Empty fitting room");
                        fittingRoom.closeFittingRoom();
                    }else{
                        fittingRoom.exitRoom(this);
                    }

                    //<<<END OF CRITICAL SECTION>>>
                }
                //Release semaphore permit for other threads to use.
                s.release();
            }
        } catch (InterruptedException e) {
            System.out.println(selfStr() + ": " + e.getLocalizedMessage());
        }
        return;
    }

    /**
     * Check if the Person has already been fitted.
     * @return True if fitted, false if otherwise.
     */
    public boolean isFitted(){
        return this.fitted;
    }

    /**
     * Set a person's room number
     * @param roomNo
     */
    public void setRoomNo(int roomNo){
        this.roomNo = roomNo;
    }

    /**
     * Get the room number a person is in.
     * @return Room no.
     */
    public int getRoomNo(){
        return this.roomNo;
    }

    /**
     * Get the ID of the person
     * @return ID of the person
     */
    public long getID(){
        return this.getId();
    }

    /**
     * Get the color of the person
     * @return Color of the person
     */
    public String getColor(){
        return this.color;
    }

    public long getFittingTime(){
        return this.fittingTime;
    }

    /**
     * Get the basic stringified details of the person 
     * @return
     */
    public String selfStr(){
        return getId() + " (" + getColor() + ", " + getFittingTime() + "ms) ";
    }

    /**
     * Print the stringified version if the Person obj.
     */
    public void printSelf(){
        System.out.println(selfStr());
    }
}