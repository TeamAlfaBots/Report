import asyncio
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

class MassReportEngine:
    def __init__(self, db_session):
        self.db = db_session

    async def attack(self, target_id, target_type, reason_key):
        accounts = self.db.query(Account).filter(Account.is_active == 1).all()
        if not accounts: return "No accounts!"

        tasks = []
        for acc in accounts:
            tasks.append(self._single_report_task(acc, target_id, target_type, reason_key))
        
        await asyncio.gather(*tasks)
        return "Attack Finished!"

    async def _single_report_task(self, acc, target_id, target_type, reason_key):
        client = TelegramClient(StringSession(acc.session_string), acc.api_id, acc.api_hash)
        try:
            await client.connect()
            reason = self._map_reason(reason_key)
            if target_type == 'user':
                await client.request(functions.account.ReportPeerRequest(peer=target_id, reason=reason, message="DeepHat"))
            else:
                await client.request(functions.channels.ReportRequest(peer=target_id, reason=reason, message="DeepHat"))
            await asyncio.sleep(3)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await client.disconnect()

    def _map_reason(self, reason_key):
        mapping = {"spam": types.InputReportReasonSpam(), "violence": types.InputReportReasonViolence()}
        return mapping.get(reason_key, types.InputReportReasonSpam())
