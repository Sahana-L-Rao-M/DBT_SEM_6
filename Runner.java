import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class Runner implements Runnable {
    private String name;
    private int distance;

    public Runner(String name) {
        this.name = name;
        this.distance = 0;
    }

    public void run() {
        Random random = new Random();
        while (distance < 1000) {
            distance += random.nextInt(6) + 5;
            System.out.println(name + " has run " + distance + " meters");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public int getDistance() {
        return distance;
    }

    public String getName() {
        return name;
    }

    public static void main(String[] args) {
        int numRunners = Integer.parseInt(args[0]);
        List<Runner> runners = new ArrayList<Runner>();

        for (int i = 1; i <= numRunners; i++) {
            runners.add(new Runner("Runner " + i));
        }

        List<Thread> threads = new ArrayList<Thread>();
        for (Runner runner : runners) {
            Thread thread = new Thread(runner);
            threads.add(thread);
            thread.start();
        }

        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        Collections.sort(runners, (r1, r2) -> r2.getDistance() - r1.getDistance());
        System.out.println("Top 3 runners:");
        for (int i = 0; i < 3; i++) {
            System.out.println(runners.get(i).getName() + " - " + runners.get(i).getDistance() + " meters");
        }
    }
}
