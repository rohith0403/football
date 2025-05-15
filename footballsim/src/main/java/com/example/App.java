package com.example;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );
        Player player1 = new Player();
        player1.setName("Player 1");
        player1.setNationality("ENG");
        System.out.println(player1);
    }
}
