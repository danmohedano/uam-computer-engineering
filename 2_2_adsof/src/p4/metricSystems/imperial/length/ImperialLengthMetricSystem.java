/**
 * 
 */
package p4.metricSystems.imperial.length;

import java.util.Collection;
import java.util.List;
import p4.metricSystems.*;
import p4.units.*;

/**
 * Imperial Length Metric System. Units: Foot, Inch, Yard, Mile
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public final class ImperialLengthMetricSystem extends AbstractMetricSystem implements IMetricSystem {
	public static final IPhysicalUnit FOOT = new BasicUnit(1, Quantity.LENGTH, "ft");
	public static final IPhysicalUnit INCH = new BasicUnit(1/12, Quantity.LENGTH, "in");
	public static final IPhysicalUnit YARD = new BasicUnit(3, Quantity.LENGTH, "yd");
	public static final IPhysicalUnit MILE = new BasicUnit(5280, Quantity.LENGTH, "ml");
	
	public static final IMetricSystem SYSTEM = new ImperialLengthMetricSystem(List.of(FOOT, INCH, YARD, MILE));
	
	private ImperialLengthMetricSystem(Collection<IPhysicalUnit> x) {
		super(x);
	}
}
