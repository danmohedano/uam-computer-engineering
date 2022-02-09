/**
 * 
 */
package p4.metricSystems.si.time;

import java.util.Collection;
import java.util.List;

import p4.metricSystems.*;
import p4.units.*;

/**
 * International Time Metric System. Units: Second, Minute, Hour
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public final class SiTimeMetricSystem extends AbstractMetricSystem implements IMetricSystem {
	public static final IPhysicalUnit SECOND = new BasicUnit(1, Quantity.TIME, "s");
	public static final IPhysicalUnit MINUTE = new BasicUnit(60, Quantity.TIME, "min");
	public static final IPhysicalUnit HOUR = new BasicUnit(3600, Quantity.TIME, "h");
	
	public static final IMetricSystem SYSTEM = new SiTimeMetricSystem(List.of(SECOND, MINUTE, HOUR));
	
	private SiTimeMetricSystem(Collection<IPhysicalUnit> x) {
		super(x);
	}
}
