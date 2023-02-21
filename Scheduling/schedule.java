import java.util.*;

class process{
    private int pid;
    private int arrivalTime;
    private int burstTime;
    private boolean isIdle;
    public process(int pid, int arrivalTime, int burstTime, boolean isIdle){
        this.pid = pid;
        this.arrivalTime = arrivalTime;
        this.burstTime = burstTime;
        this.isIdle = isIdle;
    }
    public String stringSummary(){
        return "P%d: (%d, %d, %b)".formatted(this.pid, this.arrivalTime, this.burstTime, this.isIdle);
    }
    public void printSummary(){
        System.out.println(stringSummary());
    }
    public int getPID(){
        return this.pid;
    }
    public int getArrivalTime(){
        return this.arrivalTime;
    }
    public int getBurstTime(){
        return this.burstTime;
    }
    public boolean getIsIdle(){
        return this.isIdle;
    }
    public process decreaseBurst(int amount){
        this.burstTime -= amount;
        return this;
    }
}

class ganttSlot{
    private int pid;
    private int start;
    private int end;
    private int time;

    public ganttSlot(int pid, int start, int time){
        this.pid = pid;
        this.start = start;
        this.end = start + time;
        this.time = time;
    }

    public String stringSummary(){
        return "|%d--P%d(%d)--%d|".formatted(this.start, this.pid, this.time, this.end);
    }

    public void printSummary(){
        System.out.println(stringSummary());
    }
}

public class schedule {
    public static void main(String[] args){
        schedule s = new schedule();
        System.exit(0);
    }

    public schedule(){
        System.out.println("CPU Scheduling Simulator\n");

        System.out.println("Note that idles are not considered here.\n");

        ArrayList<process> processes = new ArrayList<>();
        processes.add(new process(1, 0, 20, false));
        processes.add(new process(2, 2, 4, false));
        processes.add(new process(3, 7, 6, false));
        processes.add(new process(4, 10, 12, false));

        for(int i = 0; i < processes.size(); i++){
            processes.get(i).printSummary();
        }
        System.out.println("Total Burst Time: " + getSumBurst(processes));

        ArrayList<ganttSlot> fcfsGanttChart = new ArrayList<>();
        fcfsGanttChart = fcfs(processes);
        printGanttChart(fcfsGanttChart);

        ArrayList<ganttSlot> sjfGanttChart = new ArrayList<>();
        sjfGanttChart = fcfs(processes);
        printGanttChart(sjfGanttChart);
    }

    public ArrayList<ganttSlot> sjf(ArrayList<process> processes){
        /**
         * Schedule algorithms used first->last depending on condition: SJF->FCFS
         * Key objectives: 
         * 1. Non-preemptively arrange processes such that shortest time will be first.
         * 2. Should there be processes that have the same burst time, schedule those specifically by fcfs.
        */
        System.out.println("\nSJF+FCFS");
        ArrayList<ganttSlot> ganttChart = new ArrayList<>();
        int wait = 0;

        return ganttChart;
    }

    /**
     * Implementation of a simple FCFS algorithm.
     * Assumes no idle processes.
     * @param processes ArrayList of processes to produced a gantt chart from. Assumes sort by pid.
     */
    public ArrayList<ganttSlot> fcfs(ArrayList<process> processes){
        System.out.println("\nFCFS");
        ArrayList<ganttSlot> ganttChart = new ArrayList<>();
        int wait = 0;
        while(processes.size() > 0){
            ganttSlot newSlot = new ganttSlot(processes.get(0).getPID(), wait, processes.get(0).getBurstTime());
            wait += processes.get(0).getBurstTime();
            processes.set(0, processes.get(0).decreaseBurst(processes.get(0).getBurstTime()));
            ganttChart.add(newSlot);
            processes = removeFinished(processes);
        }
        return ganttChart;
    }

    private void printGanttChart(ArrayList<ganttSlot> ganttChart){
        for(int i = 0; i < ganttChart.size(); i++){
            System.out.print(ganttChart.get(i).stringSummary());
        }
        System.out.println("");
    }

    private int getSumBurst(ArrayList<process> processes){
        int sum = 0;
        for(int i = 0; i < processes.size(); i++){
            sum += processes.get(i).getBurstTime();
        }
        return sum;
    }

    private ArrayList<process> removeFinished(ArrayList<process> processes){
        ArrayList<process> filtered = new ArrayList<>();
        for(int i = 0; i < processes.size(); i++){
            if(processes.get(i).getBurstTime() != 0){
                filtered.add(processes.get(i));
            }
        }
        return filtered;
    }
}