import java.util.ArrayList;
import java.util.Scanner;

public class driver{
    public static void main(String[] args){
        cls();
        System.out.println("THREADING\n");
        System.out.println("Creates a thread pool whose object searches\nusing random value that is prime.\n\nA thread will only stop if\nthe random value is a prime no.\n");

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter no. of threads: ");
        int threadCount = Integer.parseInt(sc.nextLine());
        ArrayList<Thread> objectList = new ArrayList<Thread>();

        //Build threaded objects
        System.out.println("Building threads...");
        for(int i = 0; i < threadCount; i++)
            objectList.add(new Thread(new object(i)));

        //Start threads
        System.out.println("Starting threads...");
        for(int j = 0; j < threadCount; j++){
            objectList.get(j).start(); //use start and not run
        }

        //Await for threads to end
        boolean stillRunning = true;
        while(stillRunning){
            int running = 0;
            for(int j = 0; j < threadCount; j++){
                if(objectList.get(j).isAlive())
                    running++;
            }
            if(running == 0){
                System.out.println("Threads Finished!");
                stillRunning = false;
            }else{
                System.out.println("Threads Running: " + running + "/" + threadCount);
            }
            cls();
        }
    }
    private static void cls(){
        //Clear Screen Code
    }
}