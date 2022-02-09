/**
 * 
 */
package p4.units;

import p4.magnitude.exceptions.*;
import p4.metricSystems.IMetricSystem;

/**
 * Class that implements the IPhysicalUnit interface
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public class BasicUnit implements IPhysicalUnit {
	private double baseWeight;
	private Quantity quantity;
	private String abbrev;
	private IMetricSystem sys;
	
	public BasicUnit(double baseWeight, Quantity quantity, String abbrev)
	{
		this.baseWeight = baseWeight;
		this.quantity = quantity;
		this.abbrev = abbrev;
	}
	
	/**
	 * Calculates if the transformation between the units can be made or not
	 * @param u - target unit
	 * @return true if the transformation is possible
	 */
	@Override
	public boolean canTransformTo(IPhysicalUnit u) {
		if (this.quantity.equals(u.getQuantity())) {
			if (this.sys.equals(u.getMetricSystem())) return true;
			else if (this.sys.getConverter(u.getMetricSystem()) != null) return true;
		}
		return false;
	}
	
	/**
	 * Basic transformation between units. Ignores converters
	 * @param d - value of the unit
	 * @param u - target unit
	 * @return value after the transformation
	 * @throws InvalidQuantitiesException - if the quantities don't match
	 * @throws UnknownUnitException - if the transformation is invalid between the units
	 */
	@Override
	public double transformTo(double d, IPhysicalUnit u) throws QuantityException {
		if (!(this.quantity.equals(u.getQuantity()))) throw new InvalidQuantitiesException(this, u);
		if (!(this.sys.equals(u.getMetricSystem()))) throw new UnknownUnitException(this, u);
		return d * this.baseWeight / ((BasicUnit)u).baseWeight;
	}

	/**
	 * @return the quantity
	 */
	@Override
	public Quantity getQuantity() {
		return quantity;
	}

	/**
	 * @return the abbreviation 
	 */
	@Override
	public String abbrev() {
		return abbrev;
	}

	@Override
	public String toString()
	{
		return abbrev + " " + quantity;
	}

	/**
	 * @return the metric system
	 */
	@Override
	public IMetricSystem getMetricSystem() {
		return sys;
	}
	
	/**
	 * Sets the metric system of the unit
	 * @param x - metric system
	 */
	public void setMetricSystem(IMetricSystem x) { this.sys = x;}

}
