package p4.test;

import p4.metricSystems.IMetricSystem;
import p4.metricSystems.imperial.length.ImperialLengthMetricSystem;
import p4.metricSystems.si.length.SiLengthMetricSystem;

public class MetricSystemTest {

	public static void main(String[] args) {
		IMetricSystem ms = SiLengthMetricSystem.SYSTEM;
		//new SiLengthMetricSystem();	// daría error de compilación
		System.out.println(ms.units());
		System.out.println("Base = "+ms.base());
		
		System.out.println(SiLengthMetricSystem.METER.canTransformTo(ImperialLengthMetricSystem.FOOT));	// No: different metric systems
	}

}
