/**
 * 
 */
package p4.magnitude;

import p4.magnitude.exceptions.QuantityException;
import p4.units.IPhysicalUnit;

/**
 * Interface to handle Magnitudes
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public interface IMagnitude {
	IMagnitude add(IMagnitude m) throws QuantityException;
	IMagnitude subs(IMagnitude m) throws QuantityException;
	IMagnitude transformTo(IPhysicalUnit c) throws QuantityException;
	IPhysicalUnit getUnit();
	double getValue();
}
