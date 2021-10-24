import React from "react";
import AboutCard from "./AboutCard";
import { Flex, useColorModeValue } from "@chakra-ui/react";
import { MdHeadset } from "react-icons/md";
import { HiOutlineSparkles } from "react-icons/hi";

import zac from "../assets/zac.jpg";
import george from "../assets/george.jpg";
import hargun from "../assets/hargun.jpg";

function About() {
  return (
    <div>
      <Flex
        bg={useColorModeValue("white", "gray.800")}
        px={50}
        py={50}
        w="full"
        alignItems="center"
        justifyContent="center"
        flexWrap="wrap"
      >
        <AboutCard
          name="Zac Waite"
          role_emoji={MdHeadset}
          image={zac}
          emoji_color="white"
          role_description="Project Manager and Backend Developer"
          description="Student athlete and insomniac web/robot programmer"
          university="uWaterloo Software Engineering"
          email="zwaite@uwaterloo.ca"
        />
        <AboutCard
          name="George Shao"
          role_emoji={HiOutlineSparkles}
          image={george}
          emoji_color="yellow"
          role_description="Frontend Developer"
          description="Hackathon Fanatic & 2x VC Grantee"
          university="uWaterloo Software Engineering"
          email="g6shao@uwaterloo.ca"
        />
        <AboutCard
          name="Steven Gong"
          role_emoji={MdHeadset}
          image="https://thispersondoesnotexist.com/image"
          emoji_color="white"
          role_description="Role"
          description="[Placeholder description] Full Stack maker & UI / UX Designer , love hip hop music Author of
          Building UI."
          university="uWaterloo Software Engineering"
          email="userid@uwaterloo.ca"
        />
        <AboutCard
          name="Hargun Mujral"
          role_emoji={MdHeadset}
          image={hargun}
          emoji_color="white"
          role_description="Arduino and Data Processing"
          description="16 year old math nerd and EDM fanatic"
          university="uWaterloo Software Engineering"
          email="hmujral@uwaterloo.ca"
        />
        <AboutCard
          name="Michael Dennisov"
          role_emoji={MdHeadset}
          image="https://thispersondoesnotexist.com/image"
          emoji_color="white"
          role_description="Role"
          description="[Placeholder description] Full Stack maker & UI / UX Designer , love hip hop music Author of
          Building UI."
          university="uWaterloo Software Engineering"
          email="userid@uwaterloo.ca"
        />
      </Flex>
    </div>
  );
}

export default About;
