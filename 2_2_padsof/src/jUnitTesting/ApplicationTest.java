package jUnitTesting;

import static org.junit.Assert.*;

import java.util.*;

import org.junit.*;

import application.Application;
import compositePattern.RegisteredCitizen;

public class ApplicationTest {
	RegisteredCitizen member;
	RegisteredCitizen member2;
	@Before
	public void setUp() throws Exception {
		member = new RegisteredCitizen("Rachel Tyrell", "onl", "Nexus-07", false);
		member2 = new RegisteredCitizen("Joe", "impswd", "0KD6-3.7", false);
	}
	
	@After
	public void After() {
		RegisteredCitizen.setAllCitizens(new TreeSet<>());
	}

	@Test (expected = Exception.class)
	public void testLoginandLogOutTtwice() throws Exception {
		assertFalse(Application.login("pepito", "bruh"));
		assertTrue(Application.login("admin", "admin"));
		Application.logout();
		Application.logout();
	}

	@Test (expected = Exception.class)
	public void testLoginTwice() throws Exception {
		assertTrue(Application.login("Joe", "impswd"));
		Application.login("pepito", "bruh");
	}

}
