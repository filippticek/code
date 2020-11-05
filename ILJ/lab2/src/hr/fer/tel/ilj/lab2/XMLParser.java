package hr.fer.tel.ilj.lab2;

import javax.xml.stream.XMLEventReader;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.events.*;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.lang.reflect.Array;
import java.util.Iterator;
import java.util.Scanner;

public class XMLParser {
    public static void main(String[] args) {
        boolean bElement = false;
        boolean bText = false;


        Scanner sc = new Scanner(System.in);

        while (sc.hasNextLine() ){
            String line = sc.nextLine();
            String element = "";
            String value = "";
            String times = "";
            int count = 0;
            if (line.equals("EXIT")) {
                System.exit(0);
            } else {
                element = line.split(" ")[0];
                value = line.split(" ")[1];
                times = line.split(" ")[2];

                if (times.equals("*")) {
                    count = -1;
                } else {
                    count = Integer.parseInt(times);
                }

                if (element.equals("ELEMENT") || element.equals("TEXT")) {
                    value = value.substring(1, value.length() - 1);
                }
            }

            try {
                XMLInputFactory factory = XMLInputFactory.newInstance();
                XMLEventReader eventReader =
                        factory.createXMLEventReader(new FileReader("input.xml"));

                while(eventReader.hasNext() && count != 0) {
                    XMLEvent event = eventReader.nextEvent();
                    int child = 0;

                    switch(event.getEventType()) {
                        case XMLStreamConstants.START_ELEMENT:
                            StartElement startElement = event.asStartElement();
                            String qName = startElement.getName().getLocalPart();



                            switch (element){
                                case "ELEMENT":
                                    if (qName.equalsIgnoreCase(value)) bElement = true;

                                    if (bElement) System.out.println(startElement);

                                    break;
                                case "ATTRIBUTE":
                                    Iterator<Attribute> attr = event.asStartElement().getAttributes();
                                    while(attr.hasNext()){
                                        if (count == 0) {
                                            continue;
                                        }
                                        Attribute myAttribute = attr.next();

                                        if(myAttribute.getName().toString().equals(value)){
                                            count--;
                                            System.out.println(myAttribute.getValue());
                                        }
                                    }
                                    break;
                                case "TEXT":
                                    //if (bText) System.out.println(startElement);

                                    if (qName.equalsIgnoreCase(value)) bText = true;

                                    if (bText && !qName.equalsIgnoreCase(value)) child++;

                                    break;
                            }

                            break;

                        case XMLStreamConstants.CHARACTERS:
                            Characters characters = event.asCharacters();

                            switch (element){
                                case "ELEMENT":
                                    if (bElement) System.out.println(characters);
                                    break;
                                case "ATTRIBUTE":
                                    continue;
                                case "TEXT":
                                    if (bText && child == 0) System.out.println(characters);
                                    break;
                            }

                            break;

                        case XMLStreamConstants.END_ELEMENT:
                            EndElement endElement = event.asEndElement();

                            switch (element){
                                case "ELEMENT":
                                    if (bElement) System.out.println(endElement);

                                    if (endElement.getName().getLocalPart()
                                            .equalsIgnoreCase(value)) {
                                        count--;
                                        bElement = false;
                                    }
                                    break;
                                case "ATTRIBUTE":
                                    continue;
                                case "TEXT":
                                    if (endElement.getName().getLocalPart()
                                            .equalsIgnoreCase(value)){
                                        count--;
                                        bText = false;
                                    }

                                    //if (bText) System.out.println(endElement);
                                    break;
                            }

                            break;
                    }
                }
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (XMLStreamException e) {
                e.printStackTrace();
            }
        }
    }
}

