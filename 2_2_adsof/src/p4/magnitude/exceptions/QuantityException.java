/**
 * 
 */
package p4.magnitude.exceptions;

import p4.units.IPhysicalUnit;

/**
 * Generic quantity exception for Practice 4
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
@SuppressWarnings("serial")
public abstract class QuantityException extends Exception {
	protected IPhysicalUnit u1;
	protected IPhysicalUnit u2;
	
	public QuantityException(IPhysicalUnit u1, IPhysicalUnit u2)
	{
		this.u1 = u1;
		this.u2 = u2;
	}
}
