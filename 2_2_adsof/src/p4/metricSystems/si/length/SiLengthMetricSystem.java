/**
 * 
 */
package p4.metricSystems.si.length;

import java.util.Collection;
import java.util.List;
import p4.metricSystems.*;
import p4.units.*;

/**
 * International Length Metric System. Units: Meter, Kilometer, Millimeter
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public final class SiLengthMetricSystem extends AbstractMetricSystem implements IMetricSystem {
	public static final IPhysicalUnit METER = new BasicUnit(1, Quantity.LENGTH, "m");
	public static final IPhysicalUnit KILOMETER = new BasicUnit(1000, Quantity.LENGTH, "km");
	public static final IPhysicalUnit MILLIMETER = new BasicUnit(0.001, Quantity.LENGTH, "mm");
	
	public static final IMetricSystem SYSTEM = new SiLengthMetricSystem(List.of(METER, KILOMETER, MILLIMETER));
	
	private SiLengthMetricSystem(Collection<IPhysicalUnit> x) {
		super(x);
	}
}
