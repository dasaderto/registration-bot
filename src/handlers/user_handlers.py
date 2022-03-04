from src.framework.handlers import prepare_ctx, HandlerContext, BaseStateMachine
from src.framework.localization import L
from src.persistence.user import UserRoles
from src.services.user_service import UserService, UserKeyboardService
from src.states.user_states import UserState


class UserStateMachine(BaseStateMachine):
    keyboard_service = UserKeyboardService()

    async def _process_phone_setup(self):
        keyboard = self.keyboard_service.user_phone_getting_keyboard()
        await UserState.phone_number.set()
        await self.ctx.message.answer(L('handlers.user_phone_number.main_message'), reply_markup=keyboard)

    async def _process_role_setup(self):
        await UserState.user_role.set()
        keyboard = self.keyboard_service.user_setup_role_keyboard()
        await self.ctx.message.answer(L('handlers.user_role_setup.main_message'), reply_markup=keyboard)

    async def start(self):
        user = await self.ctx.user
        if not user.phone:
            await self._process_phone_setup()
            return
        if not user.role:
            await self._process_role_setup()
            return

        await self.ctx.state.finish()


@prepare_ctx(state_machine=UserStateMachine)
async def user_phone_number_handler(ctx: HandlerContext):
    await ctx.state.update_data(phone_number=ctx.message.contact.phone_number)
    user = await ctx.user
    await UserService(db=ctx.db).update(user=user, phone=ctx.message.contact.phone_number)
    await ctx.message.answer(L('handlers.user_phone_number.success'))


@prepare_ctx(state_machine=UserStateMachine)
async def user_role_setup_handler(ctx: HandlerContext):
    if not UserRoles.has(value=ctx.message.text):
        await ctx.message.answer(L("handlers.errors.user_role_undefined"))
        return
    user = await ctx.user
    await ctx.state.update_data(user_role=ctx.message.text)
    await UserService(db=ctx.db).update(user=user, role=ctx.message.text)
    await ctx.message.answer(L("handlers.user_role_setup.success_message", role=ctx.message.text))


@prepare_ctx(state_machine=UserStateMachine)
async def start_command(ctx: HandlerContext):
    await ctx.message.answer(L("commands.start"))