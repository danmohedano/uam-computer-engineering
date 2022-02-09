/**
 * 
 */
package exception.projectExceptions;


/**
 * Superclass for all possible exceptions encountered when creating a project and submitting invalid information.
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class InvalidInfoProjectException extends GenericProjectException {
	protected String invalidInfo;
	public InvalidInfoProjectException(String invalidInfo) {
		this.invalidInfo = invalidInfo;
	}
	
	public String toString() {
		return invalidInfo;
	}

}
