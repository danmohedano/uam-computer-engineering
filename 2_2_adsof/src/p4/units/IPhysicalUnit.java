/**
 * 
 */
package p4.units;

import p4.magnitude.exceptions.QuantityException;
import p4.metricSystems.IMetricSystem;

/**
 * Interface to handle Physical Units
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public interface IPhysicalUnit {
	boolean canTransformTo(IPhysicalUnit u);
	double 	transformTo(double d, IPhysicalUnit u) throws QuantityException;
	Quantity getQuantity();
	String abbrev();
	String toString();
	IMetricSystem getMetricSystem();
	void setMetricSystem(IMetricSystem x);
}
