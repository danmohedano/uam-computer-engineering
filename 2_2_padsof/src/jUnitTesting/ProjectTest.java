package jUnitTesting;

import static org.junit.Assert.*;

import java.io.IOException;
import java.util.*;


import org.junit.*;

import application.Admin;
import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import es.uam.eps.sadp.grants.CCGG;
import es.uam.eps.sadp.grants.InvalidIDException;
import es.uam.eps.sadp.grants.InvalidRequestException;
import modifiableDates.ModifiableDate;
import project.*;
import exception.projectExceptions.*;


public class ProjectTest {
	RegisteredCitizen user1;
	RegisteredCitizen user2;
	RegisteredCitizen user3;
	
	SocialIssuesProject project1;
	InfrastructureProject project2;
	Group group1;
	Group group2;
	@Before
	public void setUp() throws Exception {
		user1 = new RegisteredCitizen("Northern", "egg", "01234567", false);
		user2 = new RegisteredCitizen("Kate", "Tomo", "16849753", false);
		user3 = new RegisteredCitizen("Lion", "Ryuka", "17948153", false);
		project1 = new SocialIssuesProject("Project1", "Description", 88000, user1, "elite", true);
		group1 = new Group("Group lovers", user1);
		group2 = new Group("SubGroup Lovers!", user1, group1);
		group1.addCitizen(user3);
		Admin.validate(project1, true, null);
	}
	
	@After
	public void tearDown() {
		Group.setAllGroups(new TreeSet<Group>());
		Project.setAllProjects(new TreeSet<Project>());
		RegisteredCitizen.setAllCitizens(new TreeSet<RegisteredCitizen>());
	}

	@Test (expected = PreExistingProjectException.class)
	public void testExistingProject() throws Exception{
		project2 = new InfrastructureProject("Project1", "Description2", 88, user1, "test.jpg", null);
	}
	
	@Test
	public void testSame() {
		assertTrue(project1 == Project.getAllProjects().first());
	}
	
	@Test
	public void testCheckIfVoted() throws Exception {
		assertTrue(project1.checkIfVoted(user1));
		assertFalse(project1.checkIfVoted(user2));
		project1.vote(user2);
		assertTrue(project1.checkIfVoted(user2));
		assertFalse(project1.checkIfVoted(user3));
		project1.vote(group1);
		assertTrue(project1.checkIfVoted(user3));
	}
	
	@Test (expected = InvalidActionProjectException.class)
	public void testVoteTwiceUser() throws Exception{
		project1.vote(user2);
		project1.vote(user2);
	}
	
	@Test (expected = Exception.class)
	public void testVoteGroupHierarchy() throws Exception{
		project1.vote(group1);
		project1.vote(group2);
	}
	
	@Test
	public void testPopularityReport() throws InvalidActionProjectException, Exception {
		assertEquals(project1.popularityReport(), 1);
		project1.vote(group1);
		assertEquals(project1.popularityReport(), 2);
		group2.addCitizen(user2);
		assertEquals(project1.popularityReport(), 3);
		group2.removeCitizen(user2);
		assertEquals(project1.popularityReport(), 2);
	}
	
	@Test (expected = InvalidActionProjectException.class)
	public void testSubscribe() throws InvalidActionProjectException{
		project1.addSubscriber(user2);
		assertTrue(project1.getSubscribers().contains(user2));
		project1.addSubscriber(user1);
	}
	
	@Test
	public void testUpdateStatus() throws InvalidThresholdProjectException, InvalidActionProjectException {
		Project.setThreshold(2);
		project1.vote(user3);
		project1.vote(user2);
		assertEquals(project1.getStatus(), Status.PASSED_THRESHOLD);
	}
	
	@Test
	public void testCheckDls() {
		ModifiableDate.plusDays(50);
		project1.checkDls();
		assertEquals(project1.getStatus(), Status.OUTOFDATE);
	}
	
	@Test 
	public void testUpdateDls() throws InvalidActionProjectException {
		ModifiableDate.plusDays(60);
		project1.vote(user2);
		assertNotEquals(project1.getDoc(), project1.getDls());
	}
	
	@Test 
	public void testConnection() throws InvalidActionProjectException, IOException, InvalidRequestException, InvalidThresholdProjectException, InvalidIDException {
		Project.setThreshold(2);
		project1.vote(user3);
		CCGG.getGateway().testIOException(3, false);
		CCGG.getGateway().setDate(ModifiableDate.getModifiableDate());
		project1.sendProject();
		project1.receiveFunding();
		assertNull(project1.getBudgetGranted());
		ModifiableDate.plusDays(15);
		CCGG.getGateway().setDate(ModifiableDate.getModifiableDate());
		project1.receiveFunding();
		assertNotNull(project1.getBudgetGranted());
	}
}