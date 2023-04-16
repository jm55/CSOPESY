//FittingRoom Pseudocode

import java.security.SecureRandom; //For random select of initial color
import java.util.ArrayList;
import java.util.concurrent.Semaphore;

//Room of a fittingRoom.
class Room{
	private Person p; //Person in the room
	
	public Room(){
		this.p = null;
	}
	
	//Get Person obj in room
	public Person getOccupant(){
		return this.p;
	}
	
	//Tell if occupy or not
	public boolean isOccupied(){
		if(getOccupant() == null)
			return false;
		return true;
	}
	
	//Person enters room; Called by Person itself via (this)
	public boolean enterRoom(Person p){
		if(isOccupied() || p == null) //Either room is used or no Person is given
			return false;
		this.p = p;
		return true;
	}
	
	//Person exits room; Called by Person
	public void exitRoom(){
		this.p = null;
	}
}

//FittingRoom; Threaded for independence in own process handling.
public class FittingRoom extends Thread{
	//Data handled by FittingRoom (some lent to or used by Person)
	private static Room[] rooms = null;
    private static long startTime = 0, timelimit = 0;
    private static int dominantColor = 0; //Defaults to Blue
    private static String[] colors = {"Blue", "Green"};
    private static boolean allowEntry = false, open = true;
    private static ArrayList<Person> Guests = null;
    private static Semaphore s = null;
	
	public FittingRoom(int[] nbg, long newTimeLimit, long fittingLimit){
		//Stagnant values
		rooms = new Room[nbg[0]]; //Rooms of n length
		timelimit = newTimeLimit; //Color's limit
		
		//Semaphores
		s = new Semaphore(nbg[0]); //Build Semaphores of n permits.
		
		//Activate rooms
		for(int r = 0; r < nbg[0]; r++)
			rooms[r] = new Room();
		
		//Randomly Select Initial Color
		if(new SecureRandom().nextInt(100)%2 != 0) //Odd no.
			dominantColor = 1; //Select Green
			
		//Build Guest Pool
		Guests = new ArrayList<Person>();
		for(int i = 0; i < nbg[1]; i++)
			Guests.add(new Person("Blue", s, this, fittingLimit));
		for(int i = 0; i < nbg[2]; i++)
			Guests.add(new Person("Green", s, this, fittingLimit));
	}
	
	@Override
	public void run(){
		//Run every Person Thread
		for(int g = 0;  g < Guests.size(); g++)
			Guests.get(g).start();
		
		//Mark start time of first color for switching later on.
		startTime = System.currentTimeMillis();
		
		//Allow entry of persons
		allowEntry = true;
		
		//<<START: CRITICAL SECTION>>
		
		while(open){
			//Count remaining threads (for mixture test)
			int[] rem = getRemaining();
			
			if(getRuntime() > timelimit){
				//Occupied and remaining mixture is heterogenous
				if(isOccupied() && !((rem[0]==0)^(rem[1]==0)))
					stopEntry(); //Stop entry until empty (let threads finish)
				else //Start entry for new color or IF remaining is homogenous
					startEntry(); 
			}
		}
		
		//<<END: CRITICAL SECTION>>
		
		return;
	}
	
	//Person enters a room; Called by Person via (this)
	public synchronized int enterRoom(Person p){
		//Check which room is available
		int slot = isAvailable();
		if(slot == -1) //No room available
			return slot;
			
		//Check if empty (i.e., 1st Person); State 'only'
		if(isEmpty())
			System.out.println(p.selfStr() + p.getColor() + " only");
		
		//Enter fitting room
		rooms[slot].enterRoom(p);
		System.out.println(p.selfStr());
		
		return slot; //Used by Person thread itself
	}
	
	//Person exits room; Called by Person via (this)
	public synchronized void exitRoom(Person p){
		for(int r = 0;  r < rooms.length; r++){
			if(	rooms[r].getOccupant() != null && 
				rooms[r].getOccupant().getId() == p.getId()){
				rooms[r].exitRoom();
				Guests.remove(p); //Remove from "pending" list as they are finished
			}
		}
	}
	
	//Switch color and allow entry
	public synchronized void startEntry(){
		switchColor();
		startTime = System.currentTimeMillis(); //Re-mark start time for switching.
		allowEntry = true;
	}
	
	//Stop allowing entry of persons
	public synchronized void stopEntry(){
		allowEntry = false;
	}
	
	//Count the mixture of pending Persons/threads.
	public synchronized int[] getRemaining(){
		int[] rem = {0,0};
		for(Person g : Guests){
			if(g.getColor().equalsIgnoreCase("Blue"))
                rem[0]++;
            if(g.getColor().equalsIgnoreCase("Green"))
                rem[1]++;
		}
		return rem;
	}
	
	//Check if fitting room is not occupied by anyone.
	public synchronized boolean isEmpty(){
		return !isOccupied();
	}
	
	//Check if allowed to enter; Called by Person before enterRoom(Person)
	public synchronized boolean isAllowedEntry(){
		return allowEntry;
	}
	
	//Check if Person is last on the list.
	//Will dictate whether to close fittingRoom afterwards.
	public boolean isLastPerson(Person p){
		if(Guests.size() > 1) //Other persons are still pending
			return false;
			
		for(Person g : Guests){
			if(g.getId() == p.getId() && Guests.size() == 1){
				this.exitRoom(p);
				return true;
			}
		}
		
		return false; //Necessary to write but unlikely to reach here.
	}
	
	//Check if Person matches allowed color; Called by Person via (this)
	public synchronized boolean isMatching(Person p){
		if(getColor().equalsIgnoreCase(p.getColor()))
            return true;
        else
            return false;
	}
	
	//Close fitting room; Called by Person if lastPerson is True
	public void closeFittingRoom(){
		open = false; //Stops while loop of FittingRoom thread.
	}
	
	//Switch color only if the no. of threads assoc. to the color is > 0
	public int switchColor(){
		if(dominantColor == 0 && getRemaining()[1] > 0){
            dominantColor = 1;
        }else if(dominantColor == 1 && getRemaining()[0] > 0){
            dominantColor = 0;
        }
        return dominantColor;
	}
	
	//Check if a room is available and which if True
	public int isAvailable(){
		for(int r = 0; r < rooms.length; r++)
            if(!rooms[r].isOccupied())
                return r; //Essentially the room[] index
        return -1; //No room
	}
	
	//Check if ALL rooms are occupied.
	public boolean isFull(){
		int occupied = 0;
        for(Room r : rooms)
            if(r.isOccupied())
                occupied++;
        if(occupied == rooms.length)
            return true;
        else
            return false;
	}
	
	//Check if at least ONE room is occupied.
	public boolean isOccupied(){
        for(Room r: rooms){
            if(r.isOccupied())
                return true;
        }
        return false;
    }
	
	//Get the dominant/allowed color
	public String getColor(){
        return colors[dominantColor];
    }
	
	//Get runtime of the fitting room; Used for time checking of current color
	private float getRuntime(){
		return System.currentTimeMillis() - startTime;
	}
}