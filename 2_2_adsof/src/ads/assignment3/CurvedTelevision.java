/**
 * 
 */
package ads.assignment3;

/**
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
public class CurvedTelevision extends Television {

		private Dimension dimensions;
		private double weight;
		
		public CurvedTelevision(String brand, String model, double basePrice, EnergyEfficiency efficiency, double screenSize, Dimension dimensions, double weight) {
			super(brand, model, basePrice, efficiency, screenSize);
			this.dimensions = dimensions;
			this.weight = weight;
		}

		/**
	     * Method to calculate the transport cost of the curved television
	     * @return transport cost
	     */
		public double transportCost()
	    {
			return super.transportCost() + (dimensions.volume()*25);
	    }
		
		/**
		 * @return the dimensions
		 */
		public Dimension getDimensions() {
			return dimensions;
		}

		/**
		 * @param dimensions the dimensions to set
		 */
		public void setDimensions(Dimension dimensions) {
			this.dimensions = dimensions;
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
}
