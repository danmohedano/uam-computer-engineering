/**
 * 
 */
package p4.metricSystems;

import java.util.Collection;

import p4.converter.IMetricSystemConverter;
import p4.units.IPhysicalUnit;

/**
 * Interface to handle Metric Systems
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public interface IMetricSystem {
	IPhysicalUnit base();
	Collection<IPhysicalUnit> units();
	IMetricSystemConverter getConverter(IMetricSystem to); 
}
