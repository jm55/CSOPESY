/**
 * CSOPESY - Process Scheduling
 * 
 * de Veyra, Escalona, Naval, Villavicencio
 */

import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Random;
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
        else
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
        if(isOccupied()){
            return false;
        }else{
            this.p = p;
            if(this.p != null)
                return true;
            else
                return false;
        }
    }

    /**
     * Person 'exists' the room.
     * Sets this room's p as null.
     * @return True if successfully exited, false if otherwise.
     */
    public boolean exitRoom(){
        this.p = null;
        if(isOccupied())
            return false;
        return true;
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
    private static String[] colors = null;
    private static boolean allowEntry = false;

    /**
     * Constructor for fitting room
     * @param slots How many slots/rooms will there be?
     * @param newTimeLimit What is the timelimit for any color (in ms)?
     */
    public FittingRoom(int slots, long newTimeLimit, String[] newColors){
        //Set stagnant values
        rooms = new Room[slots];
        timelimit = newTimeLimit;
        colors = newColors;

        //Activate rooms
        for(int r = 0; r < slots; r++){
            rooms[r] = new Room();
        }

        //Random Color Selection (Randomly )
        int random = new SecureRandom("CSOPESY".getBytes()).nextInt(100)%2;
        if(random == 0)
            dominantColor = 0;
        else
            dominantColor = 1;
    }

    @Override
    public void run(){
        long timer = System.currentTimeMillis();
        startTime = System.currentTimeMillis();
        allowEntry = true;
        
        System.out.println("Fitting Room - Runtime: " + getRuntime()/1000 + "/Allowed_Color: " + getDominantColor());
        while(true){
            //Checks time
            if(System.currentTimeMillis()-timer > 1000){
                timer = System.currentTimeMillis();
                System.out.println("Fitting Room - Runtime: " + getRuntime()/1000 + "/Allowed_Color: " + getDominantColor());
            }
            
            //Switches color if timelimit has been reached (prevent starvation)
            if(getRuntime() > timelimit){
                if(!isOccupied()){
                    stopEntry(false);
                }else{
                    startEntry();
                }
            }
            //Termination code for fittingRoom
            //if(!isOccupied())
            //    return;
        }
    }

    /**
     * Check if entry is allowed.
     * @return True if allowed, false if otherwise.
     */
    public boolean isAllowedEntry(){
        return allowEntry;
    }

    public int switchColor(){
        if(dominantColor == 0)
            dominantColor = 1;
        else
            dominantColor = 0;
        return dominantColor;
    }

    /**
     * Start allowing entry of persons of specified color.
     * @param newDominantColor Color of people to be allowed to enter.
     */
    public void startEntry(){
        switchColor();
        allowEntry = true;
        startTime = System.currentTimeMillis();
    }

    /**
     * Stop allowing entry of persons.
     * Will only engage if the timelimit is called or if override is true.
     * @param override Overrides timelimit requirements and immediately disallows entry.
     * @return Color that was last allowed to enter.
     */
    public String stopEntry(boolean override){
        String lastDominantColor = getDominantColor();
        if(getRuntime() > timelimit || override){
            startTime = System.currentTimeMillis();
            allowEntry = false;
        }
        return lastDominantColor;
    }

    /**
     * Get the runtime of the fitting room.
     * @return Fitting room's runtime in ms.
     */
    public float getRuntime(){
        return System.currentTimeMillis() - startTime;
    }

    /**
     * Delegate entrance of Person to any available room.
     * @param p Person entering
     * @return Index in rooms[] that the Person entered.
     */
    public int enterRoom(Person p){
        if(!isMatching(p) || isFull())
            return -1;
        int slot = isAvailable();
        rooms[slot].enterRoom(p);
        return slot;
    }

    /**
     * Delegates the exit of Person from room.
     * @param p Person exiting.
     * @return True if exitted successfully, false if otherwise.
     */
    public boolean exitRoom(Person p){
        for(int r = 0; r < rooms.length; r++){
            if(rooms[r].getOccupant().getID() == p.getID())
                return rooms[r].exitRoom();
        }
        return false;
    }

    /**
     * Delegates the exit of Person from room.
     * @param ID ID no. of the Person
     * @return True if exitted successfully, false if otherwise.
     */
    public boolean exitRoom(int ID){
        for(int r = 0; r < rooms.length; r++){
            if(rooms[r].getOccupant().getID() == ID)
                return rooms[r].exitRoom();
        }
        return false;
    }
    
    /**
     * Checks if a room is available.
     * @return Room number in base 0 (i.e., index in array).
     */
    public int isAvailable(){
        for(int r = 0; r < rooms.length; r++){
            if(!rooms[r].isOccupied())
                return r;
        }
        return -1;
    }
    
    /**
     * Checks if all of the rooms are full/occupied.
     * @return True if all rooms are occupied, false if otherwise.
     */
    public boolean isFull(){
        int occupied = 0;
        for(Room r : rooms){
            if(r.isOccupied())
                occupied++;
        }
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
        return true;
    }

    /**
     * Checks if room occupants are consistent by color.
     * @return True if "consistent", false if otherwise.
     */
    public boolean isConsistent(){
        boolean firstSample = true;
        String color = "";
        for(Room r: rooms){
            if(firstSample){
                firstSample = false;
                color = r.getOccupant().getColor();
            }else{
                if(!color.equalsIgnoreCase(r.getOccupant().getColor()))
                    return false;
            }
        }
        return true;
    }

    /**
     * Get the dominant color
     * @return String value of FittingRoom's dominant color.
     */
    public String getDominantColor(){
        return colors[dominantColor];
    }

    /**
     * Checks if a Person matches the dominant color for the fitting room.
     * @param p Person to be checked.
     * @return True if matching, false if otherwise.
     */
    public boolean isMatching(Person p){
        if(getDominantColor().equalsIgnoreCase(p.getColor()))
            return true;
        else
            return false;
    }
}