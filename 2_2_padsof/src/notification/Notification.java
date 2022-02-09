/**
 * 
 */
package notification;

import java.io.Serializable;
import java.time.LocalDate;
import modifiableDates.ModifiableDate;
import project.Project;
import project.Status;

/**
 * Notification class
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
public class Notification implements Serializable{
	private static final long serialVersionUID = 1L;
	private boolean read = false;
	private Project project;
	private Status status;
	private LocalDate dateOfCreation;
	private String reason;
	
	public Notification(Project project, Status status) {
		this.project = project;
		this.status = status;
		this.dateOfCreation = ModifiableDate.getModifiableDate();
	}
	
	public Notification(Project project, Status status, String reason) {
		this(project, status);
		this.reason = reason;
	}

	/**
	 * if the notification has already been read
	 * @return the read
	 */
	public boolean isRead() {
		return read;
	}

	/**
	 * @param read the read to set
	 */
	public void setRead(boolean read) {
		this.read = read;
	}

	/**
	 * @return the project
	 */
	public Project getProject() {
		return project;
	}

	/**
	 * @param project the project to set
	 */
	public void setProject(Project project) {
		this.project = project;
	}

	/**
	 * @return the status
	 */
	public Status getStatus() {
		return status;
	}

	/**
	 * @param status the status to set
	 */
	public void setStatus(Status status) {
		this.status = status;
	}

	/**
	 * @return the dateOfCreation
	 */
	public LocalDate getDateOfCreation() {
		return dateOfCreation;
	}
	
	/**
	 * @return the reason
	 */
	public String getReason() {
		return reason;
	}

	/**
	 * @param reason the reason to set
	 */
	public void setReason(String reason) {
		this.reason = reason;
	}

	public String toString() {
		if (reason == null) {
			return "[" + this.dateOfCreation + "] " + "The project \"" + this.project.getName() + "\"" + " has changed its status to " + this.status;
		}
		else {
			return "[" + this.dateOfCreation + "] " + "The project \"" + this.project.getName() + "\"" + " has changed its status to " + this.status + ". Reason: " + reason;
		}
	}
	
}
