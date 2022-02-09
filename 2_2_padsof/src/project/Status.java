/**
 * 
 */
package project;

/**
 * Status enum to define the status of the project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
public enum Status {
	CREATED("Created"),
	ONGOING("Ongoing"),
	OUTOFDATE("Out of date"),
	PASSED_THRESHOLD("Threshold passed"),
	WAITING("Awaiting budget"),
	APPROVED("Approved"),
	REJECTED("Rejected");
	
	private String string;
	
	private Status(String string) {this.string = string;}
	public String toString() {return this.string;}
}
