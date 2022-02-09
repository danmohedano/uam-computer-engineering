package ads.assignment3.part6;

import java.util.List;

/**
 * Refrigerator class
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public class Refrigerator extends DimensionedAppliance{
    boolean noFrost;

    public Refrigerator(String brand, String model, double basePrice, EnergyEfficiency efficiency, Dimension dim, double weight, boolean noFrost){
    	this(brand, model, basePrice, efficiency, dim, weight);
        this.noFrost = noFrost;
    }

    public Refrigerator(String brand, String model, double basePrice, EnergyEfficiency efficiency, Dimension dim, double weight){
        super(brand, model, basePrice, efficiency, dim, weight);
    }
    
    public Refrigerator(List<String> data) {
		this(data.get(0), data.get(1), Double.parseDouble(data.get(2)), EnergyEfficiency.valueOf(data.get(3)), new Dimension(data.get(4), data.get(5), data.get(6)), Double.parseDouble(data.get(7)), (data.get(8).compareTo("NoFrost") == 0));
	}

	/**
     * Method to calculate the transport cost of the refrigerator
     * @return transport cost
     */
    public double transportCost(){
        double cost = this.getDim().volume() * 70.0;
        return Math.floor(cost);
    }

    /**
     * Checks if the arguments are valid to create a Refrigerator
     * @param data - arguments
     * @return true if arguments are valid
     */
    public static boolean check(List<String> data)
    {
    	if (!data.get(8).equals("NoFrost") && !data.get(8).equals("Frost")) return false;
    	return DimensionedAppliance.check(data);
    }
}

