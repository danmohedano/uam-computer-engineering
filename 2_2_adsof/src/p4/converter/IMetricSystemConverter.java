/**
 * 
 */
package p4.converter;

import p4.magnitude.IMagnitude;
import p4.magnitude.exceptions.*;
import p4.metricSystems.IMetricSystem;
import p4.units.IPhysicalUnit;

/**
 * Interface to handle Metric System Converters
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public interface IMetricSystemConverter {
	IMetricSystem sourceSystem();
	IMetricSystem targetSystem();
	IMagnitude transformTo(IMagnitude from, IPhysicalUnit to) throws UnknownUnitException;
	IMetricSystemConverter reverse();
}
