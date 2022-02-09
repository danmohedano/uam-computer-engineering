/**
 * 
 */
package exception;

/**
 * Generic Exception class with no use. Acts as superclass of all exceptions related to the application and all its modules.
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public abstract class GenericException extends Exception {
	public GenericException() {
		super();
	}
	
	public GenericException(String string) {
		super(string);
	}
}
