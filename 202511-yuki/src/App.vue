<template>
  <div id="section-1" class="container-fluid">
    <div class="main-wrapper">
      <div class="title-wrapper">
        <h1>Yuki Tsunoda’s<br />Fight to Find<br />Himself Beyond F1</h1>
        <div class="words-by">written by<br />Christopher Morency</div>
        <div class="photography-by">Photography by<br />Ellis Earl<br />Styled By<br />Talia Restrepo</div>
      </div>
      <div class="image-wrapper">
        <video autoplay loop muted :poster="videoA">
          <source src="https://hypebeast.com/image/2025/11/19/yuki-video-01.mp4" type="video/mp4">
          </source>
        </video>
      </div>
    </div>
  </div>

  <div id="intro-section" class="container-fluid">
    <div class="main-wrapper">
      <h6>Searching for Yuki Tsunoda</h6>
      <h2 class="intro">With the world watching, the Oracle Red Bull Racing driver is fighting to hold onto
        something F1 can’t measure: himself.</h2>
    </div>
  </div>

  <div class="container-fluid paragraph-section mt-[50px] md:mt-[90px]">
    <div class="main-wrapper">
      <div class="content-wrapper">
        <p>At 8PM on a Tuesday night in Milton Keynes, United Kingdom, Yuki Tsunoda appears on-screen with the ease
          of someone accustomed to perpetual transit. The lighting is muted, the room behind him carries the neutral
          anonymity of a space used only briefly. He sits in a simply black t-shirt and a couple of Chrome Hearts
          chains he wears almost casually.</p>
        <p>That same morning he arrived from Sāo Paolo, enduring what <a href="https://www.formula1.com/en/latest/article/tsunoda-concedes-nothing-worked-in-sao-paulo-after-one-of-the-worst-weekends.5NWCW4jKmjcR3P43oEUJ1u" target="_blank">he later
            described</a> as “one of the worst weekends” of his Formula 1 career. It was a race late in the
          season defined by a double time penalty, struggles with the grip, and an overall sense of frustration.</p>
      </div>
    </div>
  </div>

  <div class="container-fluid images-section">
    <div class="main-wrapper">
      <div class="image-wrapper">
        <picture>
          <source media="(max-width: 767px)" :srcset="bannerA1" />
          <source media="(min-width: 768px)" :srcset="bannerA1" />
          <img :src="bannerA1" alt="YUKI" />
        </picture>
        <div class="caption">Jacket: Spencer Badu x Alpha Industries, Pants: _J.L-A.L_, Shoes: 424, Rings: Tom Wood,
          Necklaces: Chrome Hearts</div>
      </div>
      <div class="image-wrapper">
        <picture>
          <source media="(max-width: 767px)" :srcset="bannerA2" />
          <source media="(min-width: 768px)" :srcset="bannerA2" />
          <img :src="bannerA2" alt="YUKI" />
        </picture>
        <div class="caption">Jacket: Umbro x Slam Jam</div>
      </div>
    </div>
    <div class="mobile-caption">(Left) Jacket: Spencer Badu x Alpha Industries, Pants: _J.L-A.L_, Shoes: 424, Rings:
      Tom Wood, Necklaces: Chrome Hearts
      (Right) Jacket: Umbro x Slam Jam</div>
  </div>

  <div class="container-fluid paragraph-section mt-[30px] md:mt-[90px]">
    <div class="main-wrapper">
      <div class="content-wrapper">
        <p>The larger picture is no less complicated. Tsunoda’s seat for next season remains unconfirmed, and each race
          now carries the implicit weight of evaluation. The position he occupies, often theatrically referred to as the
          “cursed second seat” within the Oracle Red Bull Racing team orbit, is one of the most scrutinized in sport. It
          sits beside Dutch teammate Max Verstappen, now a three-time world champion, and has cycled through several
          talented drivers who struggled to withstand the comparison. Few environments ask more of a young driver, and
          fewer still allow so little margin for error.
        </p>

        <p>But the uncertainty surrounding him is hardly personal when it’s built into the DNA of Formula 1 itself.
          Driver replacements, mid-season shifts, and contract rumors are as much part of the sport as lap times.
          Careers can pivot in a single racing weekend with futures recalculated in real time.</p>

        <p>On top of this instability sits the relentless cadence of the calendar. A 24-race season spread across five
          continents compresses entire lives into transit. Cities become fleeting waypoints rather than places
          experienced. And the races themselves are only a fraction of the work. Around them form a dense orbit of
          driver commitments that include pre-race interviews, post-race media scrums, sponsor obligations, investor
          dinners, celebrity meet-and-greets, engineering briefings, and mandatory team events. Even rest itself becomes
          its own form of preparation. Beyond performance, the sport demands a steady willingness to be seen,
          interpreted, and consumed.</p>
      </div>
    </div>
  </div>

  <div class="container-fluid images-section">
    <div class="main-wrapper">
      <div class="image-wrapper">
        <picture>
          <source media="(max-width: 767px)" :srcset="bannerB1" />
          <source media="(min-width: 768px)" :srcset="bannerB1" />
          <img :src="bannerB1" alt="YUKI" />
        </picture>
      </div>
      <div class="image-wrapper">
        <picture>
          <source media="(max-width: 767px)" :srcset="bannerB2" />
          <source media="(min-width: 768px)" :srcset="bannerB2" />
          <img :src="bannerB2" alt="YUKI" />
        </picture>
        <div class="caption">Full Look: 424</div>
      </div>
    </div>
    <div class="mobile-caption">(Right) Full Look: 424</div>
  </div>

  <div class="container-fluid paragraph-section mt-[30px] md:mt-[90px]">
    <div class="main-wrapper">
      <div class="content-wrapper">
        <p>Next weekend he will be in Las Vegas, driving a street race held beneath neon lights at hours that unsettle
          even the most seasoned drivers. “I never really see the city,” says Tsunoda. “You land, you go to the track,
          you do everything, and then you leave.”
        </p>

        <p>Tsunoda, now 25, has spent his entire adult life within this machinery. Born in Sagamihara, Japan, he left
          home as a teenager to climb the European racing ladder, settling first near Bologna to stay close to the
          Racing Bulls factory and, more recently, moving to Milan, where he has now made his home. The shift quietly
          reshaped him.</p>

        <p>For years, he has been cast in a certain light: the much-loved, smallest driver on the grid who often swears
          on the radio during races and is treated — often reductively — as the sport’s comic relief. The caricature
          stuck easily. But it flattened a far more complex reality: the challenge of maturing in a system that rarely
          pauses long enough for someone to understand themselves.</p>

        <p>Now he speaks about identity with a clarity that feels hard-earned. As the parts of himself he rarely gets to
          show move forward, along with the inner work he has begun to take seriously, Tsunoda finds himself in a rare
          moment for any athlete: a season in which performance and self-definition matter in equal measure.</p>
      </div>
    </div>
  </div>

  <div class="video-section">
    <div class="main-wrapper">
      <video autoplay loop muted :poster="videoB">
        <source src="https://hypebeast.com/image/2025/11/19/yuki-video-02.mp4" type="video/mp4">
        </source>
      </video>
    </div>
  </div>

  <div class="container-fluid qa-section mt-[30px] md:mt-[90px]">
    <div class="main-wrapper">
      <div class="content-wrapper">
        <h3>Christopher Morency: Yuki, what’s up? I apologize for this dark room in Amsterdam. Looks like it’s dark
          where you are too.</h3>
        <p>Yuki Tsunoda: Yeah, same here in the U.K. I’m in Milton Keynes, close to the factory. I love it here. I
          arrived last night from Brazil. The jet lag isn’t too bad; Japan and Singapore are worse. Las Vegas will be
          tough because of the lifestyle there, but I don’t get much time to look around.</p>

        <h3>Chris: Your travel schedule is intense. In the rare moments without racing or flying, who is Yuki off the
          track?</h3>
        <p>Yuki: It depends on how many days I get between the races. After the U.K., I go back to Italy for two days,
          then straight to the U.S. again. So within those two days, I don’t really want to go out. Instead, I usually
          stay home, game with friends, and literally just try to disconnect from the world. During race weeks you’ll
          see a lot of people and have many commitments — sponsors, meet-and-greets. When I have more than a week off, I
          try to go into nature, visit places I haven’t been before, go out with friends, and enjoy good food and nice
          wines.</p>

        <h3>Chris: Is that love for the outdoors new?</h3>
        <p>Yuki: I think it came around during COVID when I was living here in Milton Keynes with nothing to do. I would
          stay home most days of the year. I was a little bit lazy, honestly. I was training, but at the same time, when
          I was home, I would be holding the gaming controller with one hand and eating food I ordered with the other. I
          started to feel like my performance wasn’t great, and when someone would ask me what I did last week, my
          answers were always the same. I wasn’t creating nice memories, just waiting for my life.</p>
        <p>My team eventually told me, “Okay, you’re too lazy. We want you to come close to the factory in Italy.”
          There, my team was controlling my schedule — which included going into nature — and I started to see the
          benefits from that. I would go hiking with friends and feel more calm and less stressed.</p>
      </div>
    </div>
  </div>

  <div class="container-fluid images-section">
    <div class="main-wrapper">
      <div class="image-wrapper">
        <picture>
          <source media="(max-width: 767px)" :srcset="bannerC1" />
          <source media="(min-width: 768px)" :srcset="bannerC1" />
          <img :src="bannerC1" alt="YUKI" />
        </picture>
        <div class="caption">Jacket: Homme Plisssé Issey Miyake</div>
      </div>
      <div class="image-wrapper">
        <picture>
          <source media="(max-width: 767px)" :srcset="bannerC2" />
          <source media="(min-width: 768px)" :srcset="bannerC2" />
          <img :src="bannerC2" alt="YUKI" />
        </picture>
        <div class="caption">Top: _J.L-A.L_, Pants: 424, Shoes: Dr. Martens, Rings: Tom Wood, Necklaces: Chrome Hearts
        </div>
      </div>
    </div>
    <div class="mobile-caption">(Left) Jacket: Homme Plisssé Issey Miyake
      (Right) Top: _J.L-A.L_, Pants: 424, Shoes: Dr. Martens, Rings: Tom Wood, Necklaces: Chrome Hearts</div>
  </div>

  <div class="container-fluid qa-section mt-[30px] md:mt-[90px]">
    <div class="main-wrapper">
      <h2>“I’ve started to figure things out. I don’t try to force myself to be funny; that just feels exhausting.”</h2>
      <div class="content-wrapper">
        <h3>Chris: Your schedule makes me think of Severance, where people’s work-self and personal-self are
          disconnected. Do you feel that separation?</h3>
        <p>Yuki: I don’t feel like I’m a completely different person. I try to be myself most of the time. Perhaps when
          I force myself to be more excited and energetic when speaking to people, it’s a bit different. In my first two
          years in Formula 1, I probably felt like a different person, but now I’ve started to figure things out. I
          don’t try to force myself to be funny; that just feels exhausting. I couldn’t be the guy who came from Formula
          2 all the time.</p>

        <h3>Chris: How did you start expressing yourself after that?</h3>
        <p>Yuki: Initially I was overthinking quite a lot of stuff, even what I would post. Now I just share my
          personality. Fans normally see me under the helmet during race weeks, so I wanted to use social media to show
          who I am outside of racing: my fashion, the food I’m eating.</p>

        <h3>Chris: Speaking of fashion, I’ve seen your IG. What do you gravitate toward?</h3>
        <p>Yuki: I like jewelry; I like Chrome Hearts a lot. There aren’t a lot of their stores in Europe, but in Japan
          it’s really big. I received presents from my friends and started wearing them. Once you get into jewelry, it’s
          endless.</p>
        <p>My style evolved quite a lot. Back in Japan, I went to a high school where I had more freedom when it came to
          what I could wear. Back then I was wearing bad hoodies and pants, and I didn’t have much money. As soon as I
          moved to Europe and into F1, I started wearing a lot of branded stuff, but I didn’t like the big logos. Yet I
          liked Dior and Supreme. I started to think I might be spending too much on fashion. I had to at least control
          it more, so I started looking more at vintage stuff.</p>
        <p>Initially my style was very streetwear, but after I moved to Milan, my style changed to fit my body. With my
          height, I have to be careful with baggy clothes. I try to be mindful of the lengths of things.</p>

        <h3>Chris: You’re 25 now and have lived several lives, it feels. What moments changed you the most?</h3>
        <p>Yuki: As an athlete, it was probably the move to Italy. The new lifestyle was completely different to what I
          was used to in the U.K., and the schedule has made me a bit different. As a person, spending more time with
          friends in the city helped me grow. I’ll see good things in each person I spend time with and try to learn
          from them. It matured me.</p>
      </div>
    </div>
  </div>

  <div class="container-fluid image-section">
    <div class="main-wrapper">
      <div class="image-wrapper">
        <picture>
          <source media="(max-width: 767px)" :srcset="bannerD" />
          <source media="(min-width: 768px)" :srcset="bannerD" />
          <img :src="bannerD" alt="YUKI" />
        </picture>
      </div>
    </div>
  </div>

  <div class="container-fluid qa-section mt-[30px] md:mt-[90px]">
    <div class="main-wrapper">
      <h2>“I want to be world champion and the fastest.”</h2>
      <div class="content-wrapper">
        <h3>Chris: What drives you day to day?</h3>
        <p>Yuki: For racing, it’s pretty clear. I want to be world champion and the fastest.</p>

        <h3>Chris: With F1 becoming more mainstream through Netflix, fashion partnerships, and new tracks and teams
          being added, has the sport evolved for the better?</h3>
        <p>Yuki: There are pros and cons. I stepped into Formula 1 when these kinds of transitions literally started.
          Especially with fashion, you didn’t see much in the first year. But Lewis Hamilton started those things. As a
          rookie, I would wear a nice jacket but wasn’t sure if I could show up with it. As F1 grew, fashion brands got
          more involved, which I believe is positive. More people are beginning to understand what kind of a person you
          are outside of the team kits and helmets. It’s a different side to what people normally see on TV.</p>

        <h3>Chris: When you go back to Japan, do you feel like you’re a different version of yourself?</h3>
        <p>Yuki: The last time I was home consistently was before I was 18. Back then I wanted to get out of my house as
          soon as possible. My personality has changed quite a lot since. The moment I went back home and spent time
          with my parents, they were exactly the same as when I left. There are a lot of things that I didn’t like about
          my family, but I also used to be the person that would add “oil on the fire.” Now I try to add water to it. I
          feel like a completely different person today, and I can bring a lot of different perspectives because I’ve
          met a lot of people around the world from different cultures and have seen how they treat family in each
          country — helping each other, spending time together. But I can be myself more when I go back to my home in
          Italy.</p>

        <h3>Chris: It’s interesting how easily we fall into old patterns.</h3>
        <p>Yuki: Yeah. Once I lived by myself and spent a lot of time around other people, I was kind of disappointed in
          myself that I was so childish.</p>
      </div>
    </div>
  </div>

  <div class="container-fluid images-section">
    <div class="main-wrapper">
      <div class="image-wrapper">
        <picture>
          <source media="(max-width: 767px)" :srcset="bannerE1" />
          <source media="(min-width: 768px)" :srcset="bannerE1" />
          <img :src="bannerE1" alt="YUKI" />
        </picture>
      </div>
      <div class="image-wrapper">
        <picture>
          <source media="(max-width: 767px)" :srcset="bannerE2" />
          <source media="(min-width: 768px)" :srcset="bannerE2" />
          <img :src="bannerE2" alt="YUKI" />
        </picture>
        <div class="caption">Top: Hypebeast x Oracle Redbull Racing x Castore Polo Shirt, Hat: Oracle Red Bull Racing
          New Era 9FORTY Las Vegas GP Night Race Cap, Shoes: Reese Cooper</div>
      </div>
    </div>
    <div class="mobile-caption">(Right) Top: Hypebeast x Oracle Redbull Racing x Castore Polo Shirt, Hat: Oracle Red
      Bull Racing New Era 9FORTY Las Vegas GP Night Race Cap, Shoes: Reese Cooper</div>
  </div>
  <div class="container-fluid qa-section mt-[30px] md:mt-[90px]">
    <div class="main-wrapper">
      <h2>“With my busy schedule, there isn’t a lot of time to sit down, relax, or take a breath. I recently lost who I
        am.”</h2>
      <div class="content-wrapper">
        <h3>Chris: Looking ahead, as you approach 30, what do you hope life looks like?</h3>
        <p>Yuki: That’s what I’m trying to figure out these days. With my busy schedule, there isn’t a lot of time to
          sit down, relax, or take a breath. I recently lost who I am. There are moments when I feel like, “I used to be
          like this, or have good things about me,” like when I was a kid. I don’t have that these days. I don’t know
          why. Those things consistently start to pop into my mind when I sit down in my house, and if there’s a quiet
          moment, I sometimes feel down. I know who I want to be, but it feels far off. I don’t know how to get there
          yet. That’s a work in progress.</p>
        <p>I’ve been working with a psychology trainer to understand myself. I enjoy learning the good traits people
          have and try to take some of that. There’s this great guy, Mason Mount, the footballer. I met him at a Grand
          Prix — I think at Silverstone or in Spain. My parents were there, and this was the first time we met. We had a
          really enjoyable chat. He wanted to say hi to my parents, which was kind. I heard good things about him,
          especially about how he treats his fans.</p>

        <h3>Chris: Sounds like a certain confidence, in a way. Knowing who you are?</h3>
        <p>Yuki: Yeah. This is a good moment because I recognize that I’m struggling a little bit, and now I’m getting
          the help. There is a side of myself that has confidence, or some kind of fake confidence, where I thought I
          could get through situations without any help, but these moments added up.</p>

        <h3>Chris: If you could look far into the future, what do you hope you will have learned from this whole crazy
          career and experience that’s made up such a large chunk of your life?</h3>
        <p>Yuki: One word: confidence. The things I went through and am going through are difficult moments, and how you
          go through them and get over these things lets you recognize something you’ve never seen before in yourself.
          It makes you stronger. I hope I gain confidence from all of it.</p>
      </div>

      <div class="container-fluid">
        <div class="content-wrapper">
          <div class="text-center uppercase text-[9px] leading-[1.3em] mt-[60px] md:mt-[70px] pb-[60px] md:pb-[70px]">Written By: Christopher
            Morency, Photographed By: Ellis Earl, Styled By: Talia Restrepo, Editor-In-Chief: Madrell Stinney, Executive
            Producer: Keana Sy, Senior Producer: Catriona McCormick, Global Creative Operations Manager: Gabriella
            Koppelman, Director of Video: Kyle Reyes, Video Producer: Afeez Amao and Anisah Moosa, Web Developer: Warren
            Lee, Web Design: phuong Le and Jacky Liu, Graphic Design: Tetiana Khvorostiana and Forrest Grenfell, Art
            Director: Nayquan Shuler, Set Design: Michael O’Connell, Photo Assistant: Charlie Williams, Fashion
            Assistant: Solenne Choi and Erik Dietz</div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import videoA from '~/assets/Video_a@2x-min.jpg';
import videoB from '~/assets/Video_b@2x-min.jpg';
import bannerA1 from '~/assets/Banner_a1@2x-min.jpg';
import bannerA2 from '~/assets/Banner_a2@2x-min.jpg';
import bannerB1 from '~/assets/Banner_b1@2x-min.jpg';
import bannerB2 from '~/assets/Banner_b2@2x-min.jpg';
import bannerC1 from '~/assets/Banner_c1@2x-min.jpg';
import bannerC2 from '~/assets/Banner_c2@2x-min.jpg';
import bannerD from '~/assets/Banner_d@2x-min.jpg';
import bannerE1 from '~/assets/Banner_e1@2x-min.jpg';
import bannerE2 from '~/assets/Banner_e2@2x-min.jpg';
</script>