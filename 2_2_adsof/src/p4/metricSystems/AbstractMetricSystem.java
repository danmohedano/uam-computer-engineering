/**
 * 
 */
package p4.metricSystems;

import java.util.Collection;
import java.util.Vector;

import p4.converter.IMetricSystemConverter;
import p4.units.IPhysicalUnit;

/**
 * Generic abstract class to implement the IMetricSystem interface
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public abstract class AbstractMetricSystem implements IMetricSystem {
	private IPhysicalUnit base;
	private Vector<IPhysicalUnit> units = new Vector<>();
	private static Vector<IMetricSystemConverter> converters = new Vector<>();
	
	protected AbstractMetricSystem(Collection<IPhysicalUnit> allUnits) {
		this.units.addAll(allUnits);
		this.base = this.units.elementAt(0);
		for (IPhysicalUnit x : allUnits) { x.setMetricSystem(this);}
	}
	
	/**
	 * @return the base unit
	 */
	@Override
	public IPhysicalUnit base() {
		return base;
	}
	
	/**
	 * @return the units
	 */
	@Override
	public Collection<IPhysicalUnit> units(){
		return units;
	}
	
	/**
	 * Adds a converter and its reverse into the registry of converters
	 * @param c - converter to add
	 */
	public static void registerConverter(IMetricSystemConverter c) {
		if (!(converters.contains(c)))
		{
			converters.add(c);
			converters.add(c.reverse());
		}
	}
	
	/**
	 * Searches for a converter from this metric system to the target metric system
	 * @param to - target metric system
	 * @return the converter
	 */
	@Override
	public IMetricSystemConverter getConverter(IMetricSystem to) {
		for (IMetricSystemConverter x : converters)
		{
			if (x.targetSystem().equals(to) && x.sourceSystem().equals(this)) return x;
		}
		return null;
	}
}
