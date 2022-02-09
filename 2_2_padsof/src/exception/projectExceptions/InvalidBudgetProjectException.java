/**
 * 
 */
package exception.projectExceptions;

/**
 * if you try an invalid budget on project
 * @author danié
 *
 */
@SuppressWarnings("serial")
public class InvalidBudgetProjectException extends InvalidInfoProjectException {
	public InvalidBudgetProjectException(double invalidInfo) {
		super(Double.toString(invalidInfo));
	}

	public String toString() {
		return "\"" + this.invalidInfo + "\"" + " is an invalid budget. Must be positive.";
	}
}
