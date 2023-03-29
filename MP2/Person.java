import java.util.concurrent.Semaphore;

public class Person extends Thread{
    private int id = -1;
    private String color = null;
    private int roomNo = -1;
    static Semaphore s = null; //All persons must recognize the same no. of semaphores, thus a static value.
    float fittingTime = 2000; //In ms
    public Person(int id, String color, Semaphore sem, FittingRoom fittingRoom){
        this.id = id;
        this.color = color;
        s = sem;
    }
    public void setRoomNo(int roomNo){
        this.roomNo = roomNo;
    }
    public int getRoomNo(){
        return this.roomNo;
    }
    public int getID(){
        return this.id;
    }
    public String getColor(){
        return this.color;
    }
    public String selfStr(){
        return "ID: " + this.id + " - " + this.color;
    }
    public void printSelf(){
        System.out.println(selfStr());
    }
    @Override
    public void run(){
        try {
            /**
             * Do continous checking of the ff. before acquiring semaphore:
             * 1. There is at least 1 room available.
             * 2. All people in the fitting rooms match this.Person's color.
             * 3. Run fittingRoom.stopEntry() to check if the timelimit has been met
             *    and at what dominant color. This is for anti-starvation purposes.
             *    If "Blue" then start with "Green"
             *    If "Green" then start with "Blue"
             */
            s.acquire();

            /**
             * Fitting room stuff here
             */

            s.release();
        } catch (Exception e) {
            System.out.println(selfStr() + ": " + e.getLocalizedMessage());
        }
        
    }
}