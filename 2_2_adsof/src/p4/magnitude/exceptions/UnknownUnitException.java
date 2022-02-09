/**
 * 
 */
package p4.magnitude.exceptions;

import p4.units.IPhysicalUnit;

/**
 * Exception thrown when an invalid transformation between units is attempted
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
@SuppressWarnings("serial")
public class UnknownUnitException extends QuantityException {

	public UnknownUnitException(IPhysicalUnit u1, IPhysicalUnit u2) {
		super(u1, u2);
	}
	
	public String toString() {
		return "Cannot transform " + this.u1 + " to " + this.u2;
	}

}
