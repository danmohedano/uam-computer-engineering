package ads.assignment3;

import java.util.List;

/**
 * Appliance class to store the common data of all appliances
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 */
public abstract class Appliance {
    private String brand;
    private String model;
    private double basePrice;
    private EnergyEfficiency efficiency;

    public Appliance(String brand, String model, double basePrice, EnergyEfficiency efficiency)
    {
        this.brand = brand;
        this.model = model;
        this.basePrice = basePrice;
        this.efficiency = efficiency;
    }

    /**
     * Checks if the arguments are valid to create an Appliance
     * @param data - arguments
     * @return true if arguments are valid
     */
    public static boolean check(List<String> data)
    {
    	try { 	Double.parseDouble(data.get(2));} 
    	catch(NumberFormatException e){ return false;}
    	
    	if (Double.parseDouble(data.get(2)) <= 0) return false;
    	
    	try {	EnergyEfficiency.valueOf(data.get(3));}
    	catch(IllegalArgumentException a) { return false;}
    	
    	return true;
    }
    /**
     * Method to calculate the transport cost of the appliance
     * @return the transport cost
     */
    public abstract double transportCost();

    /**
	 * Convert to string
	 */
    public String toString()
    {
    	return brand + " " + model + ", " + String.format("%.2f", basePrice) + " Euros";
	}

	/**
	 * Indicates whether some other appliance is "equal to" this one 
	 * @param obj - the reference object with which to compare
	 * @return true if same type of appliance and same brand and model
	 */
	@Override
	public boolean equals(Object obj)
	{
		if (obj == null || obj.getClass() != this.getClass()) return false;

		if (((Appliance)obj).brand.equals(this.brand) && ((Appliance)obj).model.equals(this.model)) return true;

		return false;
	}
	
	/**
	 * @return the brand
	 */
	public String getBrand() {
		return brand;
	}

	/**
	 * @param brand the brand to set
	 */
	public void setBrand(String brand) {
		this.brand = brand;
	}

	/**
	 * @return the model
	 */
	public String getModel() {
		return model;
	}

	/**
	 * @param model the model to set
	 */
	public void setModel(String model) {
		this.model = model;
	}

	/**
	 * @return the basePrice
	 */
	public double getBasePrice() {
		return basePrice;
	}

	/**
	 * @param basePrice the basePrice to set
	 */
	public void setBasePrice(double basePrice) {
		this.basePrice = basePrice;
	}

	/**
	 * @return the efficiency
	 */
	public EnergyEfficiency getEfficiency() {
		return efficiency;
	}

	/**
	 * @param efficiency the efficiency to set
	 */
	public void setEfficiency(EnergyEfficiency efficiency) {
		this.efficiency = efficiency;
	}   
}
