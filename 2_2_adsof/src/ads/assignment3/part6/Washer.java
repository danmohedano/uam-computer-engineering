package ads.assignment3.part6;

import java.util.List;

/**
 * Washer class
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public class Washer extends DimensionedAppliance{
    double load;
    double rpm;

    Washer(String brand, String model, double basePrice, EnergyEfficiency efficiency, Dimension dim, double weight, double load, double rpm){
        this(brand, model, basePrice, efficiency, dim, weight);
        this.load = load;
        this.rpm = rpm;
    } 

    Washer(String brand, String model, double basePrice, EnergyEfficiency efficiency, Dimension dim, double weight){
        super(brand, model, basePrice, efficiency, dim, weight);
    } 

    public Washer(List<String> data) {
    	this(data.get(0), data.get(1), Double.parseDouble(data.get(2)), EnergyEfficiency.valueOf(data.get(3)), new Dimension(data.get(4), data.get(5), data.get(6)), Double.parseDouble(data.get(7)), Double.parseDouble(data.get(8)), Double.parseDouble(data.get(9)));
	}

	/**
     * Method to calculate the transport cost of the washing machine
     * @return transport cost
     */
    public double transportCost(){
        double cost;
        if(super.getWeight() <= 50) cost = 35;
        else cost = 35 + 0.5*(super.getWeight() - 50);
        return cost;
    }
    
    /**
     * Checks if the arguments are valid to create a Washer
     * @param data - arguments
     * @return true if arguments are valid
     */
    public static boolean check(List<String> data)
    {
    	double a1, a2;
    	try {	
    		a1 = Double.parseDouble(data.get(8));
    		a2 = Double.parseDouble(data.get(9));
    	}catch(NumberFormatException e) { return false;}
    	
    	if (a1 <= 0 || a2 <= 0) return false;
    	
    	return DimensionedAppliance.check(data);
    }
}
