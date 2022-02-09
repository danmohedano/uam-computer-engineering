/**
 * 
 */
package project;

import java.io.IOException;
import java.io.Serializable;
import java.time.Duration;
import java.time.LocalDate;
import java.util.*;

import compositePattern.CompositeGroupUser;
import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import es.uam.eps.sadp.grants.CCGG;
import es.uam.eps.sadp.grants.GrantRequest;
import es.uam.eps.sadp.grants.InvalidIDException;
import es.uam.eps.sadp.grants.InvalidRequestException;
import modifiableDates.*;
import exception.projectExceptions.*;

/**
 * Project Class
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
public abstract class Project implements Serializable, Comparable<Project>, GrantRequest
{
	private static final long serialVersionUID = 1L;
	protected static SortedSet<Project> allProjects = new TreeSet<>(); //List of all available projects in the application
	private static int 	threshold = 50; //Threshold for all projects
	
	private String 		name; //Name of the project
	private String 		description; //Description of the project
	private double		money; //Money requested for the project
	private LocalDate 	doc; //Date of creation
	private LocalDate	dls; //Date last support
	private Status 		status; //Current status of the project
	private RegisteredCitizen creator; //Creator of the project
	
	private Double 		budgetGranted = null;
	private String		requestId;
	private String 		rejectionReason;
	
	private HashSet<CompositeGroupUser> composites = new HashSet<>();
	private HashSet<RegisteredCitizen> userVotes = new HashSet<>();
	private HashSet<Group> groupVotes = new HashSet<>();
	private List<RegisteredCitizen> subscribers = new ArrayList<>();
	
	
	public Project(String name, String description, double money, RegisteredCitizen creator) throws InvalidInfoProjectException, PreExistingProjectException, InvalidActionProjectException, Exception
	{
		if (name.length() > 25) throw new InvalidNameProjectException(name);
		this.name = name;
		if (description.length() > 500) throw new InvalidDescriptionProjectException(description);
		this.description = description;
		if (money <= 0) throw new InvalidBudgetProjectException(money);
		this.money = money;
		this.doc = ModifiableDate.getModifiableDate();
		this.dls = ModifiableDate.getModifiableDate();
		this.status = Status.CREATED;
		if (creator == null) throw new InvalidInfoProjectException("Invalid creator");
		this.creator = creator;
		composites.add(creator);
		userVotes.add(creator);
		this.addSubscriber(creator);
		if (!Project.allProjects.add(this)) throw new PreExistingProjectException(this);
		creator.createProject(this);
	}
	
	public Project(String name, String description, double money, RegisteredCitizen creator, Group group) throws InvalidInfoProjectException, PreExistingProjectException, Exception
	{
		this(name, description, money, creator);
		if (!(group.getRepresentative().equals(creator))) throw new InvalidInfoProjectException("Invalid creator. Must be representative of the group.");
		groupVotes.add(group);
		composites.add(group);
		group.addProject(this, true);
	}
	
	/**
	 * search a project
	 * @param contains string to search
	 * @param type of project
	 * @return list with search result
	 */
	public static List<String> projectSearch(String contains, boolean type){
		ArrayList<String> result = new ArrayList<>();
		System.out.println(contains);
		for(Project myProject: Project.allProjects) {
			if ((type && myProject instanceof InfrastructureProject) || (!type && myProject instanceof SocialIssuesProject)) {
				for(int i=0; i<myProject.getName().length()-contains.length()+2; i+=1) {
					if(myProject.getName().startsWith(contains, i) == true) {
						result.add(myProject.getName());
						break;
					}
				}
			}
		}
		return result;
	}
	
	/**
	 * Searches for a project with the given name
	 * @param name of project
	 * @return the project
	 */
	public static Project getProject(String name) {
		for (Project x : Project.allProjects)
			if (x.getName().compareTo(name) == 0) return x;
		
		return null;
	}
	
	/**
	 * Searches for projects with the given status
	 * @param status - status to search for
	 * @return list of projects with that given status
	 */
	public static List<Project> projectByStatus(Status status){
		List<Project> p = new ArrayList<>();
		
		for (Project x: Project.allProjects)
			if (x.getStatus().compareTo(status) == 0) p.add(x);
		return p;
	}
	
	/**
	 * Popularity Report of a project
	 * @return score of the popularity report (number of votes)
	 */
	public long popularityReport()
	{
		long count = 0;
		for (CompositeGroupUser x : composites) {
			count += x.getUsers().size();
		}
		
		
		if (count < threshold && status.equals(Status.PASSED_THRESHOLD)) status = Status.ONGOING;
		else if (status.equals(Status.ONGOING) && count >= threshold){
			status = Status.PASSED_THRESHOLD;
			notifyAll(status);
		}
		return count;
	}
	
	/**
	 * Returns all voters of the project
	 * @return set of voters
	 */
	public HashSet<RegisteredCitizen> getAllVoters(){
		HashSet<RegisteredCitizen> totalVotes = new HashSet<>();
		HashSet<CompositeGroupUser> plzkillme = new HashSet<>();

		for(CompositeGroupUser myComp: composites) {
			for(CompositeGroupUser myUnicComp: myComp.getUsers()) {
				plzkillme.add(myUnicComp);
			}
		}
		
		for(CompositeGroupUser myUnicComp: plzkillme) {
			for(CompositeGroupUser thisisit: myUnicComp.getUsers()) {
				totalVotes.add((RegisteredCitizen)thisisit);
			}
		}

		return totalVotes;
	}
	
	/**
	 * Vote the project with a citizen
	 * @param c - citizen
	 * @throws InvalidActionProjectException if the citizen has already voted the project
	 */
	public void vote(RegisteredCitizen c) throws InvalidActionProjectException
	{
		if (!(status.equals(Status.ONGOING) || status.equals(Status.PASSED_THRESHOLD))) throw new InvalidActionProjectException("Can't vote. Project is not ongoing.");
		if (userVotes.contains(c) || this.getGroupVotesAsUsers().contains(c)) throw new InvalidActionProjectException("User has already voted the project.");
		else 
		{
			userVotes.add(c);
			composites.add(c);
			c.vote(this);
			popularityReport();
			updateDls();
		}
	}
	
	/**
	 * Vote the project with a group and all its children
	 * @param g - group
	 * @throws InvalidActionProjectException if the group has already voted the project
	 */
	public void vote(Group g) throws InvalidActionProjectException, Exception
	{
		if (!(status.equals(Status.ONGOING) || status.equals(Status.PASSED_THRESHOLD))) throw new InvalidActionProjectException("Can't vote. Project is not ongoing.");
		if (groupVotes.contains(g)) throw new InvalidActionProjectException("Group has already voted the project.");
		else
		{
			groupVotes.add(g);
			composites.add(g);
			g.addProject(this, false);
			for (Group x: g.getAllChildren()) groupVotes.add(x);
			popularityReport();
			updateDls();
		}
	}
	
	/**
	 * Returns the list of citizens subscribed to the project
	 * @return the list of citizens
	 */
	public List<RegisteredCitizen> getSubscribers()
	{
		return subscribers;
	}
	
	/**
	 * Adds a citizen as a subscriber of the project
	 * @param c - citizen
	 * @throws InvalidActionProjectException if the citizen is already subscribed to the project
	 */
	public void addSubscriber(RegisteredCitizen c) throws InvalidActionProjectException
	{
		if (c == null || subscribers.contains(c)) throw new InvalidActionProjectException("User is already subscribed to the project.");
		else 
		{
			subscribers.add(c);
			c.subscribe(this);
		}
	}
	
	/**
	 * Removes a citizen as a subscriber of the project
	 * @param c - citizen
	 * @throws InvalidActionProjectException if the citizen isn't subscribed to the project
	 */
	public void removeSubscriber(RegisteredCitizen c) throws InvalidActionProjectException
	{
		if (!(subscribers.contains(c))) throw new InvalidActionProjectException("User isn't subscribed to the project.");
		else
		{
			subscribers.remove(c);
			c.unsubscribe(this);
		}
	}
	
	/**
	 * Notifies the subscribed citizens of a certain change of status
	 * @param status - Status to notify the citizens about
	 */
	public void notifyAll(Status status) {
		for (RegisteredCitizen x : subscribers) {
			x.update(this, status);
		}
	}
	
	/**
	 * Notifies the subscribed citizens of a certain change of status with a given reason
	 * @param status - Status to notify the citizens about
	 * @param reason - reason for the change of status
	 */
	public void notifyAll(Status status, String reason) {
		for (RegisteredCitizen x : subscribers) {
			x.update(this, status, reason);
		}
	}
	
	/**
	 * Returns the citizens that voted individually the project
	 * @return set of citizens that individually voted the project
	 */
	public HashSet<RegisteredCitizen> getUserVotes()
	{
		return userVotes;
	}
	
	/**
	 * Checks if the citizen has voted the project
	 * @param c - citizen
	 * @return true if they have voted the project, directly or indirectly
	 */
	public boolean checkIfVoted(RegisteredCitizen c)
	{
		return userVotes.contains(c) || this.getGroupVotesAsUsers().contains(c);
	}
	/**
	 * Returns the groups that voted the project
	 * @return set of groups that voted the project through the representative
	 */
	public HashSet<Group> getGroupVotes()
	{
		return groupVotes;
	}
	
	/**
	 * Returns all citizens that have voted the project indirectly (through the group)
	 * @return set of citizens that indirectly voted the project
	 */
	private HashSet<RegisteredCitizen> getGroupVotesAsUsers()
	{
		HashSet<RegisteredCitizen> votes = new HashSet<>();
		if (groupVotes.isEmpty()) return votes;
		for (Group x : groupVotes)
		{
			votes.addAll(x.getMembers());
			votes.add(x.getRepresentative());
		}
		return votes;
	}
	
	/**
	 * Compares two projects based on the names
	 * @param p - the project to compare
	 * @return the comparison between the names
	 */
	public int compareTo(Project p)
	{
		return this.name.compareTo(p.name);
	}
	
	
	
	/**
	 * Indicates whether some other project is "equal to" this one 
	 * @param obj - the reference object with which to compare
	 * @return true if the projects are equal
	 */
	public boolean equals(Object obj)
	{
		if (obj == null || obj.getClass() != this.getClass()) return false;

		return ((Project)obj).name.equals(this.name);
	}
	
	/**
	 * Returns a hash code for this project
	 * @return a hash code value for this project
	 */
	public int hashCode()
	{
		if(this.name == null) return super.hashCode();
		return name.hashCode();
	}
	
	/**
	 * Getter for the size of the project list
	 * @return total of project
	 */
	public static int getNumberProjects()
	{
		return Project.allProjects.size();
	}
	
	/**
	 * Getter for the list of projects created
	 * @return sorted set of projects
	 */
	public static SortedSet<Project> getAllProjects()
	{
		return Project.allProjects;
	}
	
	/**
	 * Setter for the list of projects created
	 * @param set - the set of projects
	 */
	public static void setAllProjects(SortedSet<Project> set)
	{
		Project.allProjects = set;
	}
	
	/**
	 * @return the threshold
	 */
	public static int getThreshold() {
		return threshold;
	}
	/**
	 * @param threshold - the threshold to set
	 * @throws InvalidThresholdProjectException - if the threshold is not greater than 0
	 */
	public static void setThreshold(int threshold) throws InvalidThresholdProjectException {
		if (threshold <= 0) throw new InvalidThresholdProjectException(threshold);
		Project.threshold = threshold;
	}
	
	/**
	 * @return the name
	 */
	public String getName() {
		return name;
	}
	/**
	 * @param name the name to set
	 */
	public void setName(String name) {
		this.name = name;
	}
	/**
	 * @return the description
	 */
	public String getDescription() {
		return description;
	}
	/**
	 * @param description the description to set
	 */
	public void setDescription(String description) {
		this.description = description;
	}
	/**
	 * @return the money
	 */
	public double getMoney() {
		return money;
	}
	/**
	 * @param money the money to set
	 */
	public void setMoney(double money) {
		this.money = money;
	}
	/**
	 * @return the doc
	 */
	public LocalDate getDoc() {
		return doc;
	}
	/**
	 * @param doc the doc to set
	 */
	public void setDoc(LocalDate doc) {
		this.doc = doc;
	}
	/**
	 * @return the dls
	 */
	public LocalDate getDls() {
		return dls;
	}
	/**
	 * @param dls the dls to set
	 */
	public void setDls(LocalDate dls) {
		this.dls = dls;
	}
	
	/*
	 * Checks the date of last support and updates the status of the project if necessary
	 */
	public void checkDls() {
		Duration diff = Duration.between(dls.atStartOfDay(), ModifiableDate.getModifiableDate().atStartOfDay());
		if (diff.toDays() > 30 && (this.status.equals(Status.ONGOING) || this.status.equals(Status.PASSED_THRESHOLD))) {
			status = Status.OUTOFDATE;
			notifyAll(status);
		}
	}
	
	/**
	 * Static function to check the date of last support of all created projects
	 */
	public static void checkDlsAllProjects() {
		for (Project x : Project.allProjects) x.checkDls();
	}
	/**
	 * Updates the date of last support for the project
	 */
	private void updateDls()
	{
		if (dls.compareTo(ModifiableDate.getModifiableDate()) < 0) dls = ModifiableDate.getModifiableDate();
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
	 * @return the creator
	 */
	public RegisteredCitizen getCreator() {
		return creator;
	}	
	
	@Override 
	public String getProjectTitle() {
		return this.name;
	}
	
	@Override
	public String getProjectDescription()
	{
		return this.description;
	}
	
	@Override
	public double getRequestedAmount()
	{
		return this.money;
	}
	
	@Override
	public abstract String getExtraData();
	
	@Override
	public abstract ProjectKind getProjectKind();
	
	/**
	 * Method to send the project to the external application and request funding.
	 * @throws InvalidActionProjectException - if the project's status is not Passed_Threshold
	 * @throws IOException - thrown by the gateway
	 * @throws InvalidRequestException - thrown by the gateway
	 */
	public void sendProject() throws InvalidActionProjectException, IOException, InvalidRequestException{
		if (!(this.status.equals(Status.PASSED_THRESHOLD))) throw new InvalidActionProjectException("Can't send project for funding. It has to reach the votes threshold or has already been sent.");
		CCGG proxy = CCGG.getGateway();
		this.requestId = proxy.submitRequest(this);
		this.status = Status.WAITING;
	}
	
	/**
	 * Method to check if the project has been granted funding
	 * @return 0 for pending projects, -1 if rejected, 1 if approved
	 * @throws IOException  - thrown by the gateway
	 * @throws InvalidIDException - thrown by the gateway
	 * @throws InvalidActionProjectException - if the project's status is not WAITING
	 */
	public int receiveFunding() throws InvalidActionProjectException, IOException, InvalidIDException {
		if (!(this.status.equals(Status.WAITING))) throw new InvalidActionProjectException("Can't receive project funding. The project has not been sent.");
		CCGG proxy = CCGG.getGateway();
		Double granted = proxy.getAmountGranted(this.requestId);
		if (granted == null) return 0;
		else if (granted == 0) {
			this.budgetGranted = granted;
			this.status = Status.REJECTED;
			notifyAll(this.status);
			return -1;
		}
		else {
			this.budgetGranted = granted;
			this.status = Status.APPROVED;
			notifyAll(this.status);
			return 1;
		}
	}

	/**
	 * @return the budgetGranted
	 */
	public Double getBudgetGranted() {
		return budgetGranted;
	}
	
	public String toString() {
		return this.name + ":\n" + "\t- Description: " + this.description + "\n\t- Creator: " + this.creator.getName() + "\n\t- Requested Money: " + this.money + "\n\t- Date of Creation: " + this.doc + "\n\t- Date of Last Support: " + this.dls + "\n\t- Votes: " + this.popularityReport() + "\n\t- Status: " + this.getStatus();
	}

	/**
	 * @return the rejectionReason
	 */
	public String getRejectionReason() {
		return rejectionReason;
	}

	/**
	 * @param rejectionReason the rejectionReason to set
	 */
	public void setRejectionReason(String rejectionReason) {
		this.rejectionReason = rejectionReason;
	}

	/**
	 * @return the requestId
	 */
	public String getRequestId() {
		return requestId;
	}
}
