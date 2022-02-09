package jUnitTesting;

import static org.junit.Assert.*;

import java.util.*;

import org.junit.*;

import application.Admin;
import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import exception.projectExceptions.InvalidThresholdProjectException;
import project.Project;
import project.SocialIssuesProject;

/**
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class UserTest {
	
	Admin admin;
	RegisteredCitizen member1;
	RegisteredCitizen member2;
	RegisteredCitizen error;
	Group group;
	SocialIssuesProject project;
	
	
	/**
	 * @throws java.lang.Exception if setup fails in new RegisteredCitizen
	 */
	@Before
	public void setUp() throws Exception {
		
		admin = Admin.getAdmin();
		member1 = new RegisteredCitizen("Juan", "passwordJuan", "12345678", false); 
		member2 = new RegisteredCitizen("Georgia", "passwordGeorgia", "87654321", false); 
		group = new Group("GeorgiasGroup", member2);
		project = new SocialIssuesProject("JuansProject", "The project Juan proposed", 200, member1, "group", true);		
	}

	
	
	@After
	public void tearDown() {
		Group.setAllGroups(new TreeSet<Group>());
		Project.setAllProjects(new TreeSet<Project>());
		RegisteredCitizen.setAllCitizens(new TreeSet<RegisteredCitizen>());
	}

	
	@Test (expected = Exception.class)
	public void testSameName() throws Exception
	{
		new RegisteredCitizen("Juan", "passwordPedro", "11223344", false);		
	}
	
	
	@Test (expected = Exception.class)
	public void testSameId() throws Exception
	{
		new RegisteredCitizen("Felix", "passwordFelix", "12345678", false);		
	}
	
 	
	@Test
	public void testCheckUser() throws Exception
	{
		assertNotNull(RegisteredCitizen.checkUser("Juan", "passwordJuan"));
		assertNotNull(RegisteredCitizen.checkUser("12345678", "passwordJuan"));
		assertNull(RegisteredCitizen.checkUser("Martha", "passwordMartha"));
	}

	
	@Test (expected = InvalidThresholdProjectException.class)
	public void testSetThreshold() throws InvalidThresholdProjectException
	{		
		Admin.setThreshold(8);
		assertEquals(Project.getThreshold(), 8);
		Admin.setThreshold(-1);
		assertNotEquals(Project.getThreshold(), -1);
	}
	
	
	@Test
	public void testValidate()
	{	
		assertTrue(Admin.validate(project, true, "because I can and because I want"));
		assertEquals(Admin.validate(project, true, "bruh IDK the reason"), false);
	}
	

	@Test 
	public void testGetAdmin()
	{
		assertEquals(Admin.getAdmin(), admin);
	}
	
	
	
	@Test 
	public void testCreateGroup() 
	{
		member1.createGroup(group);
		assertTrue(member1.checkRepresentedGroup(group));
	}
	
	
	@Test 
	public void testCreateProject() throws Exception 
	{
		member1.createProject(project);
		assertTrue(member1.checkCreatedProject(project));
	}
	
	
	@Test 
	public void testVoteProject() throws Exception 
	{
		member1.vote(project);
		assertTrue(member1.checkVotedProject(project));
	}
	
	
	@Test 
	public void testSubscribeProject() throws Exception 
	{
		member1.subscribe(project);
		assertTrue(member1.checkSubscribedProject(project));
	}
	
	
	@Test 
	public void testUnubscribeProject() throws Exception 
	{
		member1.unsubscribe(project);
		assertFalse(member1.checkSubscribedProject(project));
	}
	
	
	@Test 
	public void testAddGroup() throws Exception 
	{
		member1.addGroup(group);
		assertTrue(member1.checkJoinedGroup(group));			
	}
	
	
	@Test
	public void testRemoveGroup() throws Exception 
	{
		member1.removeGroup(group);
		assertFalse(member1.checkJoinedGroup(group));	
	}
	

	
}
