from tools import  *
from objects import *
from routines import *


#This file is for strategy

class TexasRanger(GoslingAgent):
    def run(agent):

        my_distance_to_ball = (agent.me.location - agent.ball.location).magnitude()
        foe_distance_to_ball = (agent.foes[0].location - agent.ball.location).magnitude()
        me_closer_to_ball = my_distance_to_ball < foe_distance_to_ball

        my_velocity_towards_ball = agent.me.velocity - agent.ball.velocity
        foe_velocity_towards_ball = agent.foes[0].velocity - agent.ball.velocity
        me_higher_velocity_towards_ball = my_velocity_towards_ball.magnitude() > foe_velocity_towards_ball.magnitude()

        my_boost_higher_than_opponent = agent.me.boost > agent.foes[0].boost
        have_twenty_or_more_boost = agent.me.boost >= 20
        boost_is_closer_than_ball_to_my_goal = agent.ball.location - agent.friend_goal.location

        ball_in_left_field = (agent.ball.location.x * -agent.team) >= 1
        ball_in_right_field = (agent.ball.location.x * -agent.team) <= 0
        ball_in_center_field = not ball_in_left_field and not ball_in_right_field

        back_post_rotation = False

        if agent.team == 0:
            agent.debug_stack()
            agent.line(agent.me.location, agent.ball.location, [255, 255, 255])
            #print(me_closer_to_ball, me_higher_velocity_towards_ball)

        # gameplay logic
        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())

            # take a short shot when I will almost always reach the ball first
            elif me_closer_to_ball and me_higher_velocity_towards_ball:
                agent.push(short_shot(agent.foe_goal.location))
                print("Short Shot")
            elif not me_closer_to_ball and not have_twenty_or_more_boost:
                # make lists of big and any boosts
                boosts_big = [boost for boost in agent.boosts if boost.large and boost.active]
                boosts_any = [boost for boost in agent.boosts if boost.active]
                # are there any active big boosts?
                if len(boosts_big) > 0:
                    closest = boosts_big[0]
                    for boost in boosts_big:
                        if (boost.location - agent.me.location).magnitude() < (closest.location - agent.me.location).magnitude():
                            closest = boost
                    agent.push(goto_boost(closest, agent.ball.location))
                    back_post_rotation = True
                # are there any active small boosts?
                elif len(boosts_any) > 0:
                    closest = boosts_any[0]
                    for boost in boosts_any:
                        if (boost.location - agent.me.location).magnitude() < (closest.location - agent.me.location).magnitude():
                            closest = boost
                    agent.push(goto_boost(closest, agent.ball.location))
                    back_post_rotation = True
                # if there are somehow no boosts then we go back to net
                else:
                    back_post_rotation = True
            # if all else fails rotate then short shot
            else:
                if ball_in_right_field:
                    agent.push(goto(agent.friend_goal.left_post.flatten() + 50 * -agent.team, agent.ball.location))
                    #print("Left Post Rotation")
                elif ball_in_left_field:
                    agent.push(goto(agent.friend_goal.right_post.flatten() + 50 * -agent.team, agent.ball.location))
                    #print("Right Post Rotation")
                else:
                    agent.push(goto(agent.friend_goal.location.flatten() + 50 * -agent.team, agent.ball.location))
                    #print("Center Rotation")
                agent.push(short_shot(agent.foe_goal.location))
                print("Short Shot")






        
