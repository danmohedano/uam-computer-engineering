package p4.test;

import p4.magnitude.IMagnitude;
import p4.magnitude.Magnitude;
import p4.magnitude.exceptions.QuantityException;
import p4.metricSystems.imperial.length.ImperialLengthMetricSystem;
import p4.metricSystems.si.length.SiLengthMetricSystem;
import p4.metricSystems.si.length.converters.SiLength2ImperialConverter;


public class ConversionTest {

	public static void main(String[] args) throws QuantityException {
		Magnitude m  = new Magnitude(10, SiLengthMetricSystem.KILOMETER);
								
		IMagnitude inMiles = null;
		
		try {
			inMiles = m.transformTo(ImperialLengthMetricSystem.MILE);
		} catch (QuantityException e) {
			System.out.println(e);
		}
		SiLengthMetricSystem.registerConverter(new SiLength2ImperialConverter());	// This register the converter and the reverse
		inMiles = m.transformTo(ImperialLengthMetricSystem.MILE);
		
		System.out.println("In miles = "+inMiles);
		System.out.println("in m = "+ inMiles.transformTo(SiLengthMetricSystem.METER)); 			
	}

}
