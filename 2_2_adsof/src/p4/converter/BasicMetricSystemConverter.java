/**
 * 
 */
package p4.converter;

import p4.magnitude.IMagnitude;
import p4.magnitude.Magnitude;
import p4.magnitude.exceptions.*;
import p4.metricSystems.IMetricSystem;
import p4.units.IPhysicalUnit;

/**
 * Generic class to implement the IMetricSystemConverter interface
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public class BasicMetricSystemConverter implements IMetricSystemConverter {

	private IMetricSystem source;
	private IMetricSystem target;
	private double baseConversion;
	
	public BasicMetricSystemConverter(IMetricSystem source, IMetricSystem target, double baseConversion) {
		this.source = source;
		this.target = target;
		this.baseConversion = baseConversion;
	}

	/**
	 * Returns the source metric system of the converter
	 * @return source - source metric system
	 */
	@Override
	public IMetricSystem sourceSystem() {
		return source;
	}

	/**
	 * Returns the target metric system of the converter
	 * @return target - target metric system
	 */
	@Override
	public IMetricSystem targetSystem() {
		return target;
	}
	
	/**
	 * Returns the reverse metric system
	 * @return new metric system with reversed values
	 */
	@Override
	public IMetricSystemConverter reverse() {
		return new BasicMetricSystemConverter(target, source, 1/baseConversion);
	}

	/**
	 * Uses the converter to transform a magnitude into another unit
	 * @param from - Magnitude to transform
	 * @param to - target unit of the transformation
	 * @return new magnitude with the values after transformation
	 * @throws UnknownUnitException - if the transformation is invalid for the converter
	 */
	@Override
	public IMagnitude transformTo(IMagnitude from, IPhysicalUnit to) throws UnknownUnitException {
		if (!(source.equals(from.getUnit().getMetricSystem())) || !(target.equals(to.getMetricSystem()))) throw new UnknownUnitException(from.getUnit(), to);
		double baseSource = 0;
		try {
			baseSource = from.getUnit().transformTo(from.getValue(), source.base());
		} catch (QuantityException e) {}
		double baseTarget = baseSource * baseConversion;
		double finalValue = 0;
		try {
			finalValue = target.base().transformTo(baseTarget, to);
		} catch (QuantityException e) {}
		return new Magnitude(finalValue, to);
	}
}
