/**
 * 
 */
package p4.units;

import p4.magnitude.*;
import p4.magnitude.exceptions.*;
import p4.metricSystems.IMetricSystem;

/**
 * Imperial Length Metric System. Units: Foot, Inch, Yard, Mile
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public class CompositeUnit implements ICompositeUnit {
	public enum Operator{
		DIV("/"), MUL("*");
		private String abbrev;
		private Operator(String s) {
			this.abbrev = s;
		}
		public double operation(double x1, double x2) {
			if (this.equals(DIV)) {
				return x1/x2;
			}else {
				return x1*x2;
			}
		}
		public String toString() {
			return abbrev;
		}
	}
	
	private IPhysicalUnit leftUnit;
	private IPhysicalUnit rightUnit;
	private Operator operator;
	
	public CompositeUnit(IPhysicalUnit leftUnit, Operator operator, IPhysicalUnit rightUnit) {
		this.leftUnit = leftUnit;
		this.rightUnit = rightUnit;
		this.operator = operator;
	}

	/**
	 * Calculates if the transformation between the units can be made or not
	 * @param u - target unit
	 * @return true if the transformation is possible
	 */
	@Override
	public boolean canTransformTo(IPhysicalUnit u) {
		if (this.getClass() != u.getClass()) return false;
		return leftUnit.canTransformTo(((CompositeUnit)u).getLeftUnit()) && rightUnit.canTransformTo(((CompositeUnit)u).getRightUnit());
	}

	/**
	 * Basic transformation between composite units
	 * @param d - value of the unit
	 * @param u - target unit
	 * @return value after the transformation
	 * @throws InvalidQuantitiesException - if the quantities don't match
	 * @throws UnknownUnitException - if the transformation is invalid between the units
	 */
	@Override
	public double transformTo(double d, IPhysicalUnit u) throws QuantityException {
		if (this.getClass() != u.getClass()) throw new InvalidQuantitiesException(this, u);
		IMagnitude magLeft = new Magnitude(1, leftUnit);
		IMagnitude magRight = new Magnitude(1, rightUnit);
		magLeft = magLeft.transformTo(((CompositeUnit)u).getLeftUnit());
		magRight = magRight.transformTo(((CompositeUnit)u).getRightUnit());
		return d * operator.operation(magLeft.getValue(), magRight.getValue());
	}

	/** 
	 * Not implemented (doesn't have a use)
	 */
	@Override
	public Quantity getQuantity() {
		return null;
	}

	/**
	 * @return the abbreviation
	 */
	@Override
	public String abbrev() {
		return leftUnit + " " + operator + " " + rightUnit;
	}
	
	public String toString() {
		return leftUnit.abbrev() + " " + operator + " " + rightUnit.abbrev();
	}

	/**
	 * Not implemented (doesn't have a use)
	 */
	@Override
	public IMetricSystem getMetricSystem() {
		return null;
	}

	/**
	 * Not implemented (doesn't have a use)
	 */
	@Override
	public void setMetricSystem(IMetricSystem x) {
	}

	/**
	 * @return the left unit
	 */
	@Override
	public IPhysicalUnit getLeftUnit() {
		return leftUnit;
	}

	/**
	 * @return the right unit
	 */
	@Override
	public IPhysicalUnit getRightUnit() {
		return rightUnit;
	}

	/**
	 * @return the operator
	 */
	@Override
	public Operator getOperator() {
		return operator;
	}

}
