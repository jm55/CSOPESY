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
    private Person p;

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
    private static int dominantColor = -1;
    private static String[] colors = {"Blue", "Green"};
    private static boolean allowEntry = false;
    private static boolean open = true;
    private static ArrayList<Person> Guests = null;
    private static Semaphore s = null;

    /**
     * Constructor for fitting room
     * @param slots How many slots/rooms will there be?
     * @param newTimeLimit What is the timelimit for any color (in ms)?
     */
    public FittingRoom(int[] nbg, long newTimeLimit, long fittingLimit){
        //Set stagnant values
        rooms = new Room[nbg[0]];
        timelimit = newTimeLimit;

        //Build semaphores
        s = new Semaphore(nbg[0]);

        //Activate rooms
        for(int r = 0; r < nbg[0]; r++)
            rooms[r] = new Room();

        //Random Color Selection (Randomly )
        int random = new SecureRandom().nextInt(100)%2;
        if(random == 0)
            dominantColor = 0;
        else
            dominantColor = 1;

        Guests = new ArrayList<Person>();
        for(int i = 0; i < nbg[1]; i++)
            Guests.add(new Person("Blue", s, this, fittingLimit));
        for(int i = 0; i < nbg[2]; i++)
            Guests.add(new Person("Green", s, this, fittingLimit));

        for(int g = 0; g < Guests.size(); g++){
            Guests.get(g).start();
        }
            
    }

    long timer = System.currentTimeMillis();
    @Override
    public void run(){
        startTime = System.currentTimeMillis();
        allowEntry = true;
        
        System.out.println("Fitting Room Opened!");
        while(open){
            if(tick())
                printRemaining();

            //Switches color if timelimit has been reached (prevent starvation)
            if(getRuntime() > timelimit){
                if(isOccupied())
                    stopEntry();
                else
                    startEntry();
            }
        }
        System.out.println("Fitting Room Closed!");

        return;
    }

    /**
     * Check if the fitting room is empty (i.e., not occupied)
     * @return True if empty, false if otherwise.
     */
    public synchronized boolean isEmpty(){
        return !isOccupied();
    }

    /**
     * Check if entry is allowed.
     * @return True if allowed, false if otherwise.
     */
    public synchronized boolean isAllowedEntry(){
        return allowEntry;
    }

    public boolean isLastPerson(){
        if(Guests.size() == 0)
            return true;
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
        if(dominantColor == 0)
            dominantColor = 1;
        else
            dominantColor = 0;
        //System.out.println("Switch Color: " + this.getColor());
        return dominantColor;
    }

    /**
     * Start allowing entry of persons of specified color.
     * @param newDominantColor Color of people to be allowed to enter.
     */
    public synchronized void startEntry(){
        if(!allowEntry)
            //System.out.println("Allowing entry...");
        switchColor();     
        startTime = System.currentTimeMillis();
        allowEntry = true;
    }

    /**
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
     * Delegate entrance of Person to any available room.
     * @param p Person entering
     * @return Index in rooms[] that the Person entered.
     */
    public synchronized int enterRoom(Person p){
        int slot = isAvailable();

        if(isEmpty()){
            System.out.println(p.getId() + ": " + p.getColor() + " only");
        }

        System.out.println(p.getId() + ": " + p.getColor() + " - Fitting: " + p.getFittingTime() + "ms - ENTERING...");
        rooms[slot].enterRoom(p);

        return slot;
    }

    /**
     * Delegates the exit of Person from room.
     * @param p Person exiting.
     * @return True if exitted successfully, false if otherwise.
     */
    public synchronized void exitRoom(Person p){
        for(int r = 0; r < rooms.length; r++){
            if(rooms[r].getOccupant() != null && rooms[r].getOccupant().getID() == p.getID()){
                System.out.println(p.getId() + ": " + p.getColor() + " - Fitting: " + p.getFittingTime() + "ms - EXITING...");
                rooms[r].exitRoom();
                Guests.remove(p);
            }
        }
    }

    /**
     * Prints the remaining no. of threads not yet fitted.
     */
    public synchronized void printRemaining(){
        if(true){
            int blue = 0;
            int green = 0;
            for(Person g : Guests){
                if(g.getColor() == "Blue")
                    blue++;
                if(g.getColor() == "Green")
                    green++;
            }
            System.out.println("Remaining Guests: B=" + blue + ", G=" + green);
        }
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
     * Checks if a Person matches the dominant color for the fitting room.
     * @param p Person to be checked.
     * @return True if matching, false if otherwise.
     */
    public boolean isMatching(Person p){
        if(getColor().equalsIgnoreCase(p.getColor()))
            return true;
        else
            return false;
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
}