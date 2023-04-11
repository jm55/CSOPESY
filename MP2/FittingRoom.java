/**
 * CSOPESY - Process Scheduling
 * 
 * de Veyra, Escalona, Naval, Villavicencio
 */

import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.concurrent.Semaphore;

/**
 * Rooms found within a fitting room.
 */
class Room{
    private Person p; //Placeholder for Person in the Room.

    /**
     * Room constructor
     */
    public Room(){
        this.p = null;
    }

    /**
     * Check if this room is occupied.
     * @return True if occupied (such that Person p is not null), false if otherwise.
     */
    public boolean isOccupied(){
        if(getOccupant() == null)
            return false;
        return true;
    }

    /**
     * Get the occupant of the room as Person object.
     * @return Occupant of the room as Person object.
     */
    public Person getOccupant(){
        return this.p;
    }

    /**
     * Person 'enters' the room.
     * Sets this room's p as the person entering. 
     * @param p Person entering the room.
     * @return True if successfully entered, false if isOccupied() or not able to enter.
     */
    public boolean enterRoom(Person p){
        if(isOccupied() || p == null)
            return false;
        this.p = p;
        return true;
    }

    /**
     * Person 'exists' the room.
     * Sets this room's p as null.
     * @return True if successfully exited, false if otherwise.
     */
    public void exitRoom(){
        this.p = null;
    }
}

/**
 * Fitting Room 
 * i.e., an aggregation of rooms for fitting.
 */
public class FittingRoom extends Thread{
    private static Room[] rooms = null;
    private static long startTime = 0;
    private static long timelimit = 0;
    private static int dominantColor = 0;
    private static String[] colors = {"Blue", "Green"};
    private static boolean allowEntry = false;
    private static boolean open = true;
    private static ArrayList<Person> Guests = null;
    private static Semaphore s = null;

    /**
     * Constructor for fitting room
     * @param slots How many slots/rooms will there be?
     * @param newTimeLimit What is the timelimit for any color (in ms)?
     * @param fittingLimit What is the longest time that a person can fit?
     */
    public FittingRoom(int[] nbg, long newTimeLimit, long fittingLimit){
        //Set stagnant values
        rooms = new Room[nbg[0]];
        timelimit = newTimeLimit;

        //Build semaphores (1 for each room)
        s = new Semaphore(nbg[0]);

        //Activate rooms at a given n count
        for(int r = 0; r < nbg[0]; r++)
            rooms[r] = new Room();

        //Random Color Selection (Randomly)
        if(new SecureRandom().nextInt(100)%2 != 0)
            dominantColor = 1;

        //Build Guest Pool (combination of both Blue and Green threads/Persons)
        Guests = new ArrayList<Person>();
        for(int i = 0; i < nbg[1]; i++)
            Guests.add(new Person("Blue", s, this, fittingLimit));
        for(int i = 0; i < nbg[2]; i++)
            Guests.add(new Person("Green", s, this, fittingLimit));
    }

    @Override
    public void run(){
        //Start all persons in Guest
        for(int g = 0; g < Guests.size(); g++)
            Guests.get(g).start();

        //Mark start time which will dictate when to forcefully switch color (starvation prevention) 
        startTime = System.currentTimeMillis();

        //Allow entry of Persons to rooms
        allowEntry = true;
        System.out.println("Fitting Room Opened!");

        //<<<BEGINNING OF CRITICAL SECTION>>>

        //Runtime for fitting room until a Person() calls closeFittingRoom();
        while(open){
            //Get remaining threads that haven't fitted yet
            int[] rem = getRemaining();

            //DIAGNOSITC ONLY: Prints remaining threads every 1s.
            if(tick()){
                System.out.println("Remaining: " + "B=" + rem[0] + ", G=" + rem[1]);
            }

            //Switch the allowed color if timelimit has been reached to prevent starvation.
            if(getRuntime() > timelimit){
                /*
                 * If the room is occupied and if the blue/green threads are still heterogenous, 
                 * attempt stop entry to clear current queue.
                 * 
                 * Switch colors only if remaining threads are heterogenous
                 * 
                 * !((rem[0] == 0)^(rem[1] == 0)) is Neither Blue is 0 XOR Green is 0 (i.e., both shall not be same)
                 * If one is not empty but the other is, then it is homogenous (e.g. blue=10, green=0 || blue=0, green=3) 
                 * If both are empty/not empty, then heteregenous (e.g., blue=10, green=7 || blue=0, green=0)
                 * Example !((rem[0] == 0)^(rem[1] == 0)): 
                 * 10, 0 false NOT HETEROGENOUS
                 * 0, 10 false NOT HETEROGENOUS
                 * 3, 5 true HETEREOGENOUS
                 * 0, 0 true HETEREGENOUS (but pointless)
                */
                if(isOccupied() && !((rem[0] == 0)^(rem[1] == 0)))
                    stopEntry();
                //Else restart entry with another color
                else
                    startEntry();
            }
        }

        //<<<END OF CRITICAL SECTION>>>

        //Indicate closure once loop elapses.
        System.out.println("Fitting Room Closed!");
        return;
    }

    /**
     * SYNCHRONIZED/ACTS AS MONITOR OBJECT
     * Delegate entrance of Person to any available room.
     * @param p Person entering
     * @return Index in rooms[] that the Person entered.
     */
    public synchronized int enterRoom(Person p){
        //Find which room slot is available (room idx)
        int slot = isAvailable();
        if(slot == -1)
            return slot;

        //If the rooms are empty (i.e., first one), state the first color allowed to enter
        if(isEmpty())
            System.out.println(p.selfStr() + p.getColor() + " only");

        //Let the person enter the fitting room
        //System.out.println(p.selfStr() + "ENTERING..."); //<===COMMENT/UNCOMMENT ME TO DISABLE/ENABLE ENTRY PRINTOUTS 
        rooms[slot].enterRoom(p);
        System.out.println(p.selfStr());

        //Return roomNo. just incase
        return slot;
    }

    /**
     * SYNCHRONIZED/ACTS AS MONITOR OBJECT
     * Delegates the exit of Person from room.
     * Instigated by Person().
     * @param p Person exiting.
     * @return True if exitted successfully, false if otherwise.
     */
    public synchronized void exitRoom(Person p){
        //Iterate through all rooms and find Person p and make them exit the room.
        for(int r = 0; r < rooms.length; r++){
            if(rooms[r].getOccupant() != null && rooms[r].getOccupant().getId() == p.getId()){
                //System.out.println(p.selfStr() + "EXITING..."); //<===COMMENT/UNCOMMENT ME TO DISABLE/ENABLE EXIT PRINTOUTS 
                rooms[r].exitRoom();
                Guests.remove(p);
            }
        }
    }

    /**
     * SYNCHRONIZED/ACTS AS MONITOR OBJECT
     * Start allowing entry of persons of specified color.
     * @param newDominantColor Color of people to be allowed to enter.
     */
    public synchronized void startEntry(){
        switchColor();     
        startTime = System.currentTimeMillis();
        allowEntry = true;
    }

    /**
     * SYNCHRONIZED/ACTS AS MONITOR OBJECT
     * Stop allowing entry of persons.
     * Will only engage if the timelimit is called or if override is true.
     * @param override Overrides timelimit requirements and immediately disallows entry.
     * @return Color that was last allowed to enter.
     */
    public synchronized void stopEntry(){
        if(allowEntry)
            //System.out.println("Stopping entry...");
        allowEntry = false;
    }

    /**
     * SYNCHRONIZED/ACTS AS MONITOR OBJECT
     * Prints the remaining no. of threads not yet fitted.
     */
    public synchronized int[] getRemaining(){
        int[] rem = {0, 0}; //[0]=Blue, [1]=Green
        for(Person g : Guests){
            if(g.getColor().equalsIgnoreCase("Blue"))
                rem[0]++;
            if(g.getColor().equalsIgnoreCase("Green"))
                rem[1]++;
        }
        //System.out.println("Remaining Guests: B=" + rem[0] + ", G=" + rem[1]);
        return rem;
    }

    /**
     * SYNCHRONIZED/ACTS AS MONITOR OBJECT
     * Check if the fitting room is empty (i.e., not occupied)
     * @return True if empty, false if otherwise.
     */
    public synchronized boolean isEmpty(){
        return !isOccupied();
    }

    /**
     * SYNCHRONIZED/ACTS AS MONITOR OBJECT
     * Check if entry is allowed.
     * @return True if allowed, false if otherwise.
     */
    public synchronized boolean isAllowedEntry(){
        return allowEntry;
    }

    /**
     * SYNCHRONIZED/ACTS AS MONITOR OBJECT
     * Check if the Person is the last one in the guest list such that it would
     * indicate if the fitting room will then be closed.
     * @param p Person last to exit 
     * @return True if last person (matches the last Person in Guests)
     *          False if not last or does not match the actual last Person in Guests
     */
    public synchronized boolean isLastPerson(Person p){
        //If there are other guests, return false as it is not a 'last person situation'
        if(Guests.size() > 1)
            return false;
        
        for(Person g : Guests){
            if(g.getId() == p.getId() && Guests.size() == 1){
                this.exitRoom(p);
                return true;
            }
        }
        return false; //For some reason it did not see Person p despite it supposedly the last one.
    }

    /**
     * Checks if a Person matches the dominant color for the fitting room.
     * @param p Person to be checked.
     * @return True if matching, false if otherwise.
     */
    public synchronized boolean isMatching(Person p){
        if(getColor().equalsIgnoreCase(p.getColor()))
            return true;
        else
            return false;
    }

    /**
     * Closes the fitting room.
     */
    public void closeFittingRoom(){
        open = false;
    }

    /**
     * Switches the color allowed to enter
     */
    public int switchColor(){
        if(dominantColor == 0 && getRemaining()[1] > 0){
            dominantColor = 1;
        }else if(dominantColor == 1 && getRemaining()[0] > 0){
            dominantColor = 0;
        }
        return dominantColor;
    }

    /**
     * Checks if a room is available.
     * @return Room number in base 0 (i.e., index in array).
     */
    public int isAvailable(){
        for(int r = 0; r < rooms.length; r++)
            if(!rooms[r].isOccupied())
                return r;
        return -1;
    }
    
    /**
     * Checks if all of the rooms are full/occupied.
     * @return True if all rooms are occupied, false if otherwise.
     */
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

    /**
     * Checks if any of the rooms has a person in it.
     * @return True if a room is still occupied, false if otherwise.
     */
    public boolean isOccupied(){
        for(Room r: rooms){
            if(r.isOccupied())
                return true;
        }
        return false;
    }

    /**
     * Get the dominant color
     * @return String value of FittingRoom's dominant color.
     */
    public String getColor(){
        return colors[dominantColor];
    }

    /**
     * Get the runtime of the fitting room.
     * @return Fitting room's runtime in ms.
     */
    private float getRuntime(){
        return System.currentTimeMillis() - startTime;
    }

    /**
     * 'Ticks' every 1s
     * @return True if 1s has passed, false if otherwise
     */
    private boolean tick(){
        if(System.currentTimeMillis()-timer > 1000){
            timer = System.currentTimeMillis();
            return true;
        }else  
            return false;
    }
    long timer = System.currentTimeMillis();
}