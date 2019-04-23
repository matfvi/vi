import jp.ac.kobe_u.cs.cream.*;
import java.util.Scanner;
import java.io.InputStream;

public class JSSP {
    public int numOfJobs;
    public int numOfMachines;
    public int job_machine[][];
    public int job_pt[][];
    public IntVariable makespan;

    public void scan(InputStream in) {
	Scanner scanner = new Scanner(in);
	numOfJobs = scanner.nextInt();
	numOfMachines = scanner.nextInt();
	scanner.nextLine();
	job_machine = new int[numOfJobs][numOfMachines];
	job_pt = new int[numOfJobs][numOfMachines];
	for (int j = 0; j < numOfJobs; j++) {
	    for (int m = 0; m < numOfMachines; m++) {
		job_machine[j][m] = scanner.nextInt();
		job_pt[j][m] = scanner.nextInt();
	    }
	    scanner.nextLine();
	}
    }

    public Network getNetwork() {
	int machine_op[][] = new int[numOfMachines][numOfJobs];
	int machine_pt[][] = new int[numOfMachines][numOfJobs];
	for (int j = 0; j < job_machine.length; j++) {
	    for (int k = 0; k < job_machine[j].length; k++) {
		int m = job_machine[j][k];
		machine_op[m][j] = k;
		machine_pt[m][j] = job_pt[j][k];
	    }
	}

	Network net = new Network();
	IntDomain d = new IntDomain(0, IntDomain.MAX_VALUE);
	makespan = new IntVariable(net, d);
	net.setObjective(makespan);
	IntVariable job[][] = new IntVariable[numOfJobs][numOfMachines+1];
	for (int j = 0; j < numOfJobs; j++) {
	    for (int k = 0; k < numOfMachines; k++) {
		job[j][k] = new IntVariable(net, d);
	    }
	    job[j][numOfMachines] = makespan;
	    Sequential seq = new Sequential(net, job[j], job_pt[j]);
	}
	IntVariable machine[][] = new IntVariable[numOfMachines][numOfJobs];
	for (int m = 0; m < numOfMachines; m++) {
	    for (int j = 0; j < numOfJobs; j++) {
		int k = machine_op[m][j];
		machine[m][j] = job[j][k];
	    }
	    Serialized ser = new Serialized(net, machine[m], machine_pt[m]);
	}
	return net;
    }

    public static void main(String args[]) {
	JSSP jssp = new JSSP();
	jssp.scan(System.in);
	long timeout = 10*1000;
	Network network = jssp.getNetwork();
	if (network == null)
	    return;
	Solver solver = new DefaultSolver(network);
	Solution solution = solver.findFirst(timeout);
	int v = solution.getIntValue(jssp.makespan);
	System.out.println(v);
    }

}
