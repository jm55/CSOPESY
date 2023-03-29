/**
 * CSOPESY - Process Scheduling
 * 
 * de Veyra, Escalona, Naval, Villavicencio
 */

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
        if(this.p != null)
            return true;
        else
            return false;
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
public class FittingRoom{
    private static Room[] rooms = null;
    private static float startTime = 0;
    private static float timelimit = 0;
    private static String dominantColor = "";
    private static boolean allowEntry = false;

    /**
     * Constructor for fitting room
     * @param slots How many slots/rooms will there be?
     * @param newTimeLimit What is the timelimit for any color (in ms)?
     */
    public FittingRoom(int slots, float newTimeLimit){
        rooms = new Room[slots];
        timelimit = newTimeLimit;
    }

    /**
     * Check if entry is allowed.
     * @return True if allowed, false if otherwise.
     */
    public boolean isAllowedEntry(){
        return allowEntry;
    }

    /**
     * Start allowing entry of persons of specified color.
     * @param newDominantColor Color of people to be allowed to enter.
     */
    public void startEntry(String newDominantColor){
        startTime = System.currentTimeMillis();
        dominantColor = newDominantColor;
        allowEntry = true;
    }

    /**
     * Stop allowing entry of persons.
     * Will only engage if the timelimit is called or if override is true.
     * @param override Overrides timelimit requirements and immediately disallows entry.
     * @return Color that was last allowed to enter.
     */
    public String stopEntry(boolean override){
        String lastDominantColor = getDominantColor();
        if(getRuntime() >= timelimit || override){
            startTime = 0;
            dominantColor = "";
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
     * Delegates the exit of Person to their room.
     * @param p Person exiting.
     * @return True if exitted, successfully, false if otherwise.
     */
    public boolean exitRoom(Person p){
        for(int r = 0; r < rooms.length; r++){
            if(rooms[r].getOccupant().getID() == p.getID())
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
        return dominantColor;
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