import java.util.Scanner;
import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.ArrayList;
import java.util.Arrays;
import java.util.PriorityQueue;
import java.lang.Comparable;

public class Analysis {
    static class NGram implements Comparable<NGram> {
        String ngram;
        ArrayList<Double> data;
        double peak;
        NGram(String ngram, ArrayList<Double> data, double peak){
            this.ngram = ngram;
            this.data = data;
            this.peak = peak;
        }
        @Override
        public int compareTo(NGram o) {
            if(this.peak < o.peak) return -1;
            else if(this.peak > o.peak) return 1;
            else return 0;
        }

        @Override
        public String toString() {
            return ngram + " " + peak;
        }
    }    
    
    static ArrayList<Double> uncompress(String data){
        String[] dataArr = data.split(";");
        int power;
        try {
            power = Integer.parseInt(dataArr[0]);
        }
        catch (Exception e){
            System.out.println(data);
            return null;
        }
        ArrayList<Integer> deltas = new ArrayList<>();
        for (String s : dataArr[1].split(",")){
            deltas.add(Integer.parseInt(s, 16));
        }
        int first = deltas.get(0);
        ArrayList<Integer> timeseries = new ArrayList<>();
        timeseries.add(first);
        for (int i = 1; i < deltas.size(); i++){
            timeseries.add(timeseries.get(i-1) + deltas.get(i));
        }
        ArrayList<Double> result = new ArrayList<>();
        for (int i = 0; i < timeseries.size(); i++){
            result.add((double)timeseries.get(i) / (10000 * Math.pow(10, power)));
        }
        return result;
    }

    static ArrayList<Double> zscores(ArrayList<Double> data){
        ArrayList<Double> result = new ArrayList<>();
        double mean = 0;
        double std = 0;
        for (double d : data){
            mean += d;
        }
        mean /= data.size();
        for (double d : data){
            std += Math.pow(d - mean, 2);
        }
        std = Math.sqrt(std / data.size());
        for (double d : data){
            result.add((d - mean) / std);
        }
        return result;
    }
    static double max(ArrayList<Double> data){
        double max = data.get(0);
        for (double d : data){
            if (d > max){
                max = d;
            }
        }
        return max;
    }
    static int argmax(ArrayList<Double> arr){
        double max = arr.get(0);
        int index = 0;
        for (int i = 1; i < arr.size(); i++){
            if (arr.get(i) > max){
                max = arr.get(i);
                index = i;
            }
        }
        return index;
    }
    static double min(ArrayList<Double> data){
        double min = data.get(0);
        for (double d : data){
            if (d < min){
                min = d;
            }
        }
        return min;
    }
    static double rsquared(ArrayList<Double> x, ArrayList<Double> y){
        double sum = 0;
        for (int i = 0; i < x.size(); i++){
            sum += Math.pow(x.get(i) - y.get(i), 2);
        }
        return sum;
    }
    static double difference(ArrayList<Double> x, ArrayList<Double> y){
        double sum = 0;
        for (int i = 0; i < x.size(); i++){
            sum += x.get(i) - y.get(i);
        }
        return Math.abs(sum);
    }
    static double integral(ArrayList<Double> x){
        double sum = 0;
        for (int i = 0; i < x.size() - 1; i++){
            sum += (x.get(i) + x.get(i+1)) / 2;
        }
        return sum;
    }
    
    static void getPointiest(Scanner reader){
        PriorityQueue<NGram> pq = new PriorityQueue<>();
        int count = 0;
        while (reader.hasNextLine()) {
            String line = reader.nextLine().replace("\n", "");
            if (line.equals("")) continue;
            String[] parts = line.split("\\|");
            String ngram;
            String data;
            if (parts.length == 3){
                ngram = "|";
                data = parts[2];
            }
            else {
                ngram = parts[0];
                data = parts[1];
            }
            ArrayList<Double> timeseries = uncompress(data);
            double peak = max(zscores(timeseries));
            int n = argmax(timeseries);
            NGram ng = new NGram(ngram, timeseries, peak);
            if (n > 3 && n < timeseries.size() - 4){
                pq.add(ng);
                if (pq.size() > 10) pq.poll();
            }
            if (count % 10000 == 0){
                System.out.println("------------------------------------------------------");
                System.out.println(pq);
            }
            count++;
        }
        System.out.println("------------------------------------------------------");
        System.out.println(pq);
    }
    
    static void getClosest(Scanner reader, String s){
        PriorityQueue<NGram> pq = new PriorityQueue<>();
        ArrayList<Double> compare = uncompress(s);
        int count = 0;
        while (reader.hasNextLine()){
            String line = reader.nextLine().replace("\n", "");
            if (line.equals("")) continue;
            String[] parts = line.split("\\|");
            String ngram;
            String data;
            if (parts.length == 3){
                ngram = "|";
                data = parts[2];
            }
            else {
                ngram = parts[0];
                data = parts[1];
            }
            
            ArrayList<Double> timeseries = uncompress(data);
            double rs = rsquared(timeseries, compare); 
            
            NGram ng = new NGram(ngram, timeseries, -rs);
            pq.add(ng);
            if (pq.size() > 10) pq.poll();
            if (count % 100000 == 0){
                System.out.println("------------------------------------------------------");
                System.out.println(Arrays.toString(pq.toArray()));
            }
            count++;
        }

        System.out.println("------------------------------------------------------");
        System.out.println(Arrays.toString(pq.toArray()));
    }

    static void getClosestSigned(Scanner reader, String s){
        PriorityQueue<NGram> pq = new PriorityQueue<>();
        ArrayList<Double> compare = uncompress(s);
        int count = 0;
        while (reader.hasNextLine()){
            String line = reader.nextLine().replace("\n", "");
            if (line.equals("")) continue;
            String[] parts = line.split("\\|");
            String ngram;
            String data;
            if (parts.length == 3){
                ngram = "|";
                data = parts[2];
            }
            else {
                ngram = parts[0];
                data = parts[1];
            }
            
            ArrayList<Double> timeseries = uncompress(data);
            double rs = difference(timeseries, compare); 
            
            NGram ng = new NGram(ngram, timeseries, -rs);
            pq.add(ng);
            if (pq.size() > 10) pq.poll();
            if (count % 100000 == 0){
                System.out.println("------------------------------------------------------");
                System.out.println(Arrays.toString(pq.toArray()));
            }
            count++;
        }

        System.out.println("------------------------------------------------------");
        System.out.println(Arrays.toString(pq.toArray()));
    }
    static void closestIntegral(Scanner reader, String s){
        PriorityQueue<NGram> pq = new PriorityQueue<>();
        ArrayList<Double> compare = uncompress(s);
        int count = 0;
        while (reader.hasNextLine()){
            String line = reader.nextLine().replace("\n", "");
            if (line.equals("")) continue;
            String[] parts = line.split("\\|");
            String ngram;
            String data;
            if (parts.length == 3){
                ngram = "|";
                data = parts[2];
            }
            else {
                ngram = parts[0];
                data = parts[1];
            }
            
            ArrayList<Double> timeseries = uncompress(data);
            double i1 = integral(timeseries);
            double i2 = integral(compare);
            
            NGram ng = new NGram(ngram, timeseries, -Math.abs(i1 - i2));
            pq.add(ng);
            if (pq.size() > 10) pq.poll();
            if (count % 100000 == 0){
                System.out.println("------------------------------------------------------");
                System.out.println(Arrays.toString(pq.toArray()));
            }
            count++;
        }

        System.out.println("------------------------------------------------------");
        System.out.println(Arrays.toString(pq.toArray()));
    }
    static void getMostDieouts(Scanner reader){
        PriorityQueue<NGram> pq = new PriorityQueue<>();
        int count = 0;
        while (reader.hasNextLine()) {
            String line = reader.nextLine().replace("\n", "");
            if (line.equals("")) continue;
            String[] parts = line.split("\\|");
            String ngram;
            String data;
            if (parts.length == 3){
                ngram = "|";
                data = parts[2];
            }
            else if (parts.length > 3) continue;
            else {
                ngram = parts[0];
                data = parts[1];
            }
            // System.out.println(line);
            ArrayList<Double> timeseries = uncompress(data);
            double m = max(timeseries);
            double zeroThreshold = m / 100;
            double highThreshold = m/3;
            
            int counted = 0;
            double lastHigh = 0;
            for (int i = 1; i < timeseries.size(); i++){
                if (timeseries.get(i) < zeroThreshold && lastHigh > 0){
                    lastHigh = 0;
                    counted++;
                }
                if (timeseries.get(i-1) > highThreshold) lastHigh = 1;
            }
            NGram ng = new NGram(ngram, timeseries, counted);
            pq.add(ng);
            if (pq.size() > 10) pq.poll();

            if (count % 10000 == 0){
                System.out.println("------------------------------------------------------");
                System.out.println(pq);
            }
            count++;
        }
        System.out.println("------------------------------------------------------");
        System.out.println(pq);
    }

    public static void main(String[] args){
        
        try {
            File myObj = new File("time compressed.txt");
            Scanner myReader = new Scanner(myObj);
            // getPointiest(myReader);
            getClosest(myReader, "8;0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3ff,0,0,0,0,4c,4c,-3fe,4d,0,0,0,87,49e,1877,1b6b,fe8,f74,dd8,856,8c3,-d96,-11e5,-733,-486,-478,-1e1,201,-100,668,5d2,274,a97,f44,38b,15e5,e82,1607,174f,e23,1772,1a92,246e,681,-77f,776,af8,-148,-195");
            // getMostDieouts(myReader);
            // myReader.close();
          } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
          }
    }
}
