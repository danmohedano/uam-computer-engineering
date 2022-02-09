/**
 * 
 */
package p4.metricSystems.si.length.converters;

import p4.converter.BasicMetricSystemConverter;
import p4.metricSystems.imperial.length.ImperialLengthMetricSystem;
import p4.metricSystems.si.length.SiLengthMetricSystem;

/**
 * Converter from the International Length Metric System into the Imperial Length Metric System
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public class SiLength2ImperialConverter extends BasicMetricSystemConverter {
	private static final double METERTOFEET = 3.280839795;
	
	public SiLength2ImperialConverter()
	{
		super(SiLengthMetricSystem.SYSTEM, ImperialLengthMetricSystem.SYSTEM, METERTOFEET);
	}
}
