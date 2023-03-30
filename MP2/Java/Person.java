/**
 * CSOPESY - Process Scheduling
 * 
 * de Veyra, Escalona, Naval, Villavicencio
 */

import java.util.concurrent.Semaphore;

public class Person extends Thread{
    private int id = -1;
    private String color = null;
    private int roomNo = -1;
    private float fittingTime = 2000; //In ms
    private boolean fitted = false;
    static Semaphore s = null; //All persons must recognize the same no. of semaphores, thus a static value.

    /**
     * Constructor for a person
     * @param id
     * @param color
     * @param sem
     * @param fittingRoom
     */
    public Person(int id, String color, Semaphore sem, FittingRoom fittingRoom){
        this.id = id;
        this.color = color;
        s = sem;
    }    
    
    @Override
    public void run(){
        try {
            while(!fitted){
                 /**
                 * Check the following before acquiring:
                 * 1. There is at least 1 room available.
                 * 2. All people in the fitting rooms match this.Person's color.
                 * 3. Run fittingRoom.stopEntry() to check if the timelimit has been met
                 *    and at what dominant color. This is for anti-starvation purposes.
                 *    3.1. If "Blue" then start with "Green"
                 *    3.2. If "Green" then start with "Blue"
                 * 4. Check if already fitted or not. Do not enter if already fitted.
                 * 5. Check if allows fitting; via fittingRoom.isAllowedEntry()
                 */
                s.acquire();

                /**
                 * Fitting room stuff here
                 * 
                 * After 'finishing' what to do with the fitting room:
                 * 1. Set fitted as true.
                 * 2. Call fittingRoom.exit(this); or fittingRoom.exit(this.id);
                 * 
                 */

                /**
                 * Notes upon exit/before release():
                 * 1. Set fitted as true.
                 */
            }
            s.release();
        } catch (Exception e) {
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