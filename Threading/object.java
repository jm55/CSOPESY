import java.lang.Math;

public class object implements Runnable{
    int id;
    boolean running = true;
    
    public object(int id){
        this.id = id;
    }
    
    @Override
    public void run() {
        while (running){
            int random = (int)(Math.random()*100);
            if(isPrime(random))
                stop();
            else{
                //System.out.println("id: " + this.id + " - " + random);
                sleep();
            }
        }
    }

    //Source: https://www.programiz.com/java-programming/examples/prime-number
    public boolean isPrime(int input){
        for (int i = 2; i <= input / 2; ++i) {
            if (input % i == 0) { //nonprime
                return false;
            }
        }
        return true;
    }
    
    public void stop(){
        running = false;
    }
    
    private void sleep(){
        try {
            Thread.sleep(50);    
        } catch (Exception e) {
            System.out.println("id: " + this.id + " - " + e.getLocalizedMessage());
            stop();
        }
        
    }
}