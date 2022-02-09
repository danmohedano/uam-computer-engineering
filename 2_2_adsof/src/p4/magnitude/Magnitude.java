/**
 * 
 */
package p4.magnitude;

import p4.converter.IMetricSystemConverter;
import p4.magnitude.exceptions.*;
import p4.units.*;

/**
 * Class to implement the IMagnitude interface
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public class Magnitude implements IMagnitude {
	private double value;
	private IPhysicalUnit unit;
	
	public Magnitude(double value, IPhysicalUnit unit) {
		this.value = value;
		this.unit = unit;
	}

	/**
	 * Adds to magnitudes together and returns the result in the original magnitude's unit
	 * @param m - Second magnitude to add
	 * @return the magnitude with the values updated
	 */
	@Override
	public IMagnitude add(IMagnitude m) throws QuantityException {
		this.value += m.transformTo(this.unit).getValue();
		return this;
	}

	/**
	 * Subtracts a magnitude from another one and returns the result in the original magnitude's unit
	 * @param m - magnitude to subtract
	 * @return  the magnitude with the values updated
	 */
	@Override
	public IMagnitude subs(IMagnitude m) throws QuantityException {
		this.value -= m.transformTo(this.unit).getValue();
		return this;
	}

	/**
	 * Transforms the magnitude into another unit. Searches if the use of a converter is needed
	 * @param c - target unit
	 * @return the magnitude with the values updated
	 * @throws InvalidQuantitiesException - if the quantities don't match
	 * @throws UnknownUnitException - if the conversion between units is invalid 
	 */
	@Override
	public IMagnitude transformTo(IPhysicalUnit c) throws QuantityException {
		if (this.unit instanceof CompositeUnit || this.unit.getMetricSystem().equals(c.getMetricSystem())) {
			return new Magnitude(this.unit.transformTo(this.value, c), c);
		}
		else {
			if (!(this.unit.getQuantity().equals(c.getQuantity()))) throw new InvalidQuantitiesException(this.unit, c);
			IMetricSystemConverter converter;
			if ((converter = this.unit.getMetricSystem().getConverter(c.getMetricSystem())) == null) throw new UnknownUnitException(this.unit, c);
			return converter.transformTo(this, c);
		}
	}

	/**
	 * @return the unit
	 */
	@Override
	public IPhysicalUnit getUnit() {
		return unit;
	}

	/**
	 * @return the value
	 */
	@Override
	public double getValue() {
		return value;
	}
	
	/**
	 * @return string formatting of the magnitude
	 */
	@Override
	public String toString() {
		return value + " " + "[" + unit + "]";
	}

}
