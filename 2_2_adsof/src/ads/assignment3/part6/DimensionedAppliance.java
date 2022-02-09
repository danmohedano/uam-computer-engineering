package ads.assignment3.part6;

import java.util.List;

/**
 * Dimensioned Appliance abstract class
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public abstract class DimensionedAppliance extends Appliance {
    private double weight;
    private Dimension dim;

    DimensionedAppliance(String brand, String model, double basePrice, EnergyEfficiency efficiency, Dimension dim, double weight){
        super(brand, model, basePrice, efficiency);
        this.weight = weight;
        this.dim = dim;
    }

	/**
	 * @return the weight
	 */
	public double getWeight() {
		return weight;
	}

	/**
	 * @param weight the weight to set
	 */
	public void setWeight(double weight) {
		this.weight = weight;
	}

	/**
	 * @return the dim
	 */
	public Dimension getDim() {
		return dim;
	}

	/**
	 * @param dim the dim to set
	 */
	public void setDim(Dimension dim) {
		this.dim = dim;
	}
	
	/**
     * Checks if the arguments are valid to create a Dimensioned Appliance
     * @param data - arguments
     * @return true if arguments are valid
     */
	public static boolean check(List<String> data)
    {
		double a1, a2, a3, a4;
    	try {	
    		a1 = Double.parseDouble(data.get(4));
    		a2 = Double.parseDouble(data.get(5));
    		a3 = Double.parseDouble(data.get(6));
    		a4 = Double.parseDouble(data.get(7));
    	}catch(NumberFormatException e) { return false;}
    	
    	if (a1 <= 0 || a2 <= 0 || a3 <= 0 || a4 <= 0) return false;
    	
    	return Appliance.check(data);
    }
}

