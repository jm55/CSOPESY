import java.util.ArrayList;
import java.util.concurrent.Semaphore;

class Room{
    private Person p = null;
    public Room(Person p){
        this.p = p;
    }
    public boolean isOccupied(){
        if(this.p != null)
            return true;
        else
            return false;
    }
    public Person getOccupant(){
        return this.p;
    }
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
    public boolean exitRoom(){
        this.p = null;
        if(this.p != null)
            return false;
        return true;
    }
}

public class FittingRoom{
    private static Room[] rooms = null;
    private static float startTime = 0;
    private static float timelimit = 0;
    private static String dominantColor = "";
    public FittingRoom(int slots, float newTimeLimit){
        rooms = new Room[slots];
        timelimit = newTimeLimit;
    }
    public void startEntry(String newDominantColor){
        startTime = System.currentTimeMillis();
        dominantColor = newDominantColor;
    }
    public String stopEntry(){
        String lastDominantColor = getDominantColor();
        if(getRuntime() >= timelimit){
            startTime = 0;
            dominantColor = "";
        }
        return lastDominantColor;
    }
    public float getRuntime(){
        return System.currentTimeMillis() - startTime;
    }
    public int enterRoom(Person p){
        if(isFull(false))
            return -1;
        for(int r = 0; r < rooms.length; r++){
            if(!rooms[r].isOccupied()){
                if(rooms[r].enterRoom(p))
                    return r;
                else
                    return -1;
            }
        }
        return -1;
    }
    public boolean isFull(boolean absolute){
        if(absolute){
            /**
             * Check if rooms are absolutely full such that
             * ALL rooms are strictly filled.
             * 
             * Suggestion: 
             * To count all rooms that are room.isOccupied()
             * and compare it to rooms.length.
             */
        }else{
            for(int r = 0; r < rooms.length; r++){
                if(!rooms[r].isOccupied())
                    return false;
            }
            return true;
        }
    }
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
    private String getDominantColor(){
        return dominantColor;
    }
    public boolean isMatching(String color){
        if(getDominantColor().equalsIgnoreCase(color))
            return true;
        else
            return false;
    }
}