/**
 * CSOPESY - Process Scheduling
 * 
 * de Veyra, Escalona, Naval, Villavicencio
 */

import java.security.SecureRandom;
import java.util.concurrent.Semaphore;

public class Person extends Thread{
    private int id = -1;
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
    public Person(int id, String color, Semaphore sem, FittingRoom newFittingRoom){
        this.id = id;
        this.color = color;
        s = sem;
        fittingRoom = newFittingRoom;
        this.fittingTime = new SecureRandom().nextLong(1000, 3000);
        System.out.println(this.selfStr() + " Fitting Time: " + this.fittingTime + "ms");
    }    
    
    @Override
    public void run(){
        try {
            //Not fitted, allowed to acquire, and matches dominantcolor of fittingroom at the time.
            while(!fitted){
                 /**
                 * Check the following before acquiring:
                 * 1. There is at least 1 room available.
                 * 2. Use tryAcquire() acquiring instead of acquire() to automatically check before attempting to acquire().
                 */
                if(fittingRoom.isMatching(this) && s.tryAcquire()){
                    this.roomNo = fittingRoom.enterRoom(this);
                    System.out.println(this.selfStr() + " acquired semaphore! (" + s.availablePermits() + ")");
                    Thread.sleep(fittingTime);
                    this.fitted = true;
                    fittingRoom.exitRoom(this);
                    System.out.println(this.selfStr() + " finished fitting (" + this.fittingTime + "ms)");
                    /**
                     * Notes upon exit/before release():
                     * 1. Set fitted as true.
                     * 2. If last person, set FittingRoom's open as false;
                     */
                }
            }
            s.release();
        } catch (InterruptedException e) {
            System.out.println(selfStr() + ": " + e.getLocalizedMessage());
        }
        
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
    public int getID(){
        return this.id;
    }

    /**
     * Get the color of the person
     * @return Color of the person
     */
    public String getColor(){
        return this.color;
    }

    /**
     * Get the basic stringified details of the person 
     * @return
     */
    public String selfStr(){
        return "ID: " + this.id + " - " + this.color + " @ Room: " + this.roomNo;
    }

    /**
     * Print the stringified version if the Person obj.
     */
    public void printSelf(){
        System.out.println(selfStr());
    }
}