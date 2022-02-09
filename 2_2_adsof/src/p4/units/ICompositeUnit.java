/**
 * 
 */
package p4.units;

import p4.units.CompositeUnit.Operator;

/**
 * Interface to handle Composite Units 
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public interface ICompositeUnit extends IPhysicalUnit {
	Operator getOperator();
	IPhysicalUnit getLeftUnit();
	IPhysicalUnit getRightUnit();
}
